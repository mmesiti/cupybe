#!/usr/bin/env python3
##################################################################
# Author    : Dr Chennakesava Kadapa
# Date      : 02-Apr-2020
# Copyright : @SA2C
##################################################################
#
# Usage:
#
# barchartNfuncs.py <cubex-filename>  <metric>  <exclincl>  <nfuncs>
# <cubex-filename> : name of the .cubex file
# <metric>         : visits, time, max_time, min_time
# <exclincl>       : T = Exclusive, F = Inclusive
# <nfuncs>         : number of functions to plot
#
# Example:
#
# python3  barchartNfuncs.py  profile.cubex  time T  10
#
################################################################################
"""
Variant of barchartFuncwise.py, where we select the MPI calls that
were performed inside a particular function, recursively, and plot
a barchart showing the time spent in each kind of MPI function.
"""
if __name__ == "__main__":
    import merger as mg
    import index_conversions as ic
    import matplotlib.pyplot as plt
    import calltree as ct
    import os

    data_dir = "../test_data"
    inpfilename = os.path.join(data_dir, "profile-5m-nproc40-nsteps10.cubex")
    metric = "time"
    exclincl = False
    callpathid = 56

    funcname = "initia_"

    output_i = mg.process_cubex(inpfilename, exclusive=exclincl)

    call_tree = output_i.ctree

    func_node = next(
        node for node in ct.iterate_on_call_tree(call_tree) if node.fname == funcname
    )

    # and selecting the names of the functions in the subtree that start with "MPI"
    children_names = [
        node.fname + "," + str(node.cnode_id)
        for node in ct.iterate_on_call_tree(func_node, 1)
        if node.fname.startswith("MPI")
    ]

    # We convert the Cnode IDs to short callpaths in the dataframe.
    df_i = ic.convert_index(output_i.df, output_i.ctree_df, target="Short Callpath")

    res_df = df_i.loc[children_names]

    res = (
        res_df.reset_index()[["Short Callpath", "Thread ID", metric]]
        .groupby("Short Callpath")
        .sum()
        .sort_values([metric], ascending=False)[metric]
    )

    res = res.head(11 if len(res) > 11 else len(res))

    res.plot(kind="bar")

    plt.xlabel(
        "Function name: " + funcname, fontsize=12, color="blue", fontweight="bold"
    )
    plt.title(
        "metric: "
        + metric
        + " "
        + ("(Exclusive)" if exclincl == True else "(Inclusive)"),
        fontsize=12,
    )
    plt.ylabel("Time [s]", fontsize=12)

    plt.legend("", frameon=False)

    plt.tight_layout()
    plt.yscale("log")
    plt.xticks(rotation=80)
    plt.show()
