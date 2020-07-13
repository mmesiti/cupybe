#!/usr/bin/env python3

import calltree as ct
import merger as mg
import calltree_conversions as cc
import metrics as mt

import pandas as pd
import test_utils as tu
from glob import glob

def test_convert_df_to_inclusive_multi():
    '''
    This test checks that the function to compute the inclusive data from the 
    exclusive data yields the same values as the ones obtained from `cube_dump`
    using the 'incl' flag.
    ''' 
    input_files = glob(f"{tu.SCALASCA_OUTPUT}/*/profile.cubex")
    
    
    output_excl = mg.process_multi(input_files,exclusive = True)
    output_incl = mg.process_multi(input_files,exclusive = False)
    
    common_excl  = output_excl.common.sort_index()
    common_incl  = output_incl.common.sort_index()
    
    noncommon_excl  = output_excl.noncommon.sort_index()
    noncommon_incl  = output_incl.noncommon.sort_index()
    
    
    convertible_metrics = output_excl.conv_info
    calltree = output_excl.ctree
    
    # common 
    # dataframe conversions
    print("Common metrics:")
    common_excl = cc.select_metrics( common_excl, convertible_metrics)
    common_incl_comp = cc.convert_df_to_inclusive(common_excl, calltree).sort_index()
    
    common_incl = cc.select_metrics(common_incl, convertible_metrics)
    
    assert (common_excl.values != common_incl.values).any()
    print("Inclusive and exclusive results partially differ as expected.")
    assert (common_excl.values == common_incl.values).any()
    print("Inclusive and exclusive results are partially equal as expected.")
    
    tu.check_float_equality(common_incl_comp,common_incl)
    
    print( "Results from convert_df_to_inclusive coincide"
        " with the ones coming from cube_dump.")
    
    # noncommon 
    # dataframe conversions
    print("Non common metrics:")
    noncommon_excl = cc.select_metrics( noncommon_excl, convertible_metrics)
    noncommon_incl_comp = cc.convert_df_to_inclusive(noncommon_excl, calltree).sort_index()
    
    noncommon_incl = cc.select_metrics(noncommon_incl, convertible_metrics)
    
    assert (noncommon_excl.values != noncommon_incl.values).any()
    print("Inclusive and exclusive results partially differ as expected.")
    assert (noncommon_excl.values == noncommon_incl.values).any()
    print("Inclusive and exclusive results are partially equal as expected.")
    
    tolerance = 3e-3
    tu.check_float_equality(noncommon_incl_comp,noncommon_incl, tolerance )

    print( "Results from convert_df_to_inclusive coincide"
        "with the ones coming from cube_dump.\n"
        f"(with tolerance up to {tolerance})")

if __name__ == '__main__':
    test_convert_df_to_inclusive_multi()
