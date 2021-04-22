'''
Python wrapper to encode with MPEG G-PCC standard
Author: Haiqiang Wang
Data: 04/22/2021
'''

import os
import re
import subprocess


def make_cfg(gpcc_bin_path, ref_path, cfg_dir, output_dir, g, c):

    if not os.path.exists(cfg_dir):
        os.makedirs(cfg_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    src_name = re.split('/|\.', ref_path)[-2]
    recon_name = '{src}_g_{g}_c_{c}'.format(src=src_name, g=g, c=c)
    recon_path = os.path.join(output_dir, '{}.ply'.format(recon_name))
    bin_path = os.path.join(output_dir, '{}.bin'.format(recon_name))
    log_path = os.path.join(output_dir, '{}.log'.format(recon_name))
    cfg_path = os.path.join(cfg_dir, '{}.cfg'.format(recon_name))

    rst = []
    rst.append('uncompressedDataPath: {}'.format(ref_path))
    rst.append('reconstructedDataPath: {}'.format(recon_path))
    rst.append('compressedStreamPath: {}'.format(bin_path))
    rst.append('mode: 0')
    rst.append('trisoupNodeSizeLog2: 0')
    rst.append('mergeDuplicatedPoints: 1')
    rst.append('neighbourAvailBoundaryLog2: 8')
    rst.append('intra_pred_max_node_size_log2: 6')
    rst.append('srcResolution: 0')
    rst.append('outputResolution: 0')
    rst.append('maxNumQtBtBeforeOt: 4')
    rst.append('minQtbtSizeLog2: 0')
    rst.append('planarEnabled: 1')
    rst.append('planarModeIdcmUse: 0')
    rst.append('convertPlyColourspace: 1')
    rst.append('transformType: 1')
    rst.append('qpChromaOffset: 0')
    rst.append('bitdepth: 8')
    rst.append('positionQuantizationScale: {}'.format(g))   
    rst.append('qp: {}'.format(c))
    rst.append('attribute: color')

    with open(cfg_path, 'w') as f:
        for line in rst:
            f.write("%s\n" % line)

    cmd = "{exec_path} --config={cfg_path} >> {log_path}".format(exec_path=gpcc_bin_path, cfg_path=cfg_path, log_path=log_path)
    # print(cmd)

    return cmd


def process_one_depth(gpcc_bin_path, ref_dir, cfg_dir, output_dir, seq, g, c):
    cmd = []
    for _seq in seq:
        ref_path = os.path.join(ref_dir, _seq)
        for _g in g:
            for _c in c:
                _cmd = make_cfg(gpcc_bin_path, ref_path, cfg_dir, output_dir, _g, _c)
                cmd.append(_cmd)
    return cmd


if __name__ == '__main__':

    gpcc_bin_path = '../../mpeg-pcc-tmc13/build/tmc3/tmc3'
    ref_dir = '../../data/mpeg/ref/'
    cfg_dir = './cfg'
    output_dir = './ply'
    

    seq_15 = ['loot.ply']
    g_15 = [1.0, 1.0/512, 1.0/256, 1.0/64, 1.0/32, 1.0/8, 1.0/4]

    seq_14 = ['loot.ply']
    g_14 = [1.0, 1.0/256, 1.0/128, 1.0/64, 1.0/16, 1.0/8, 1.0/4]

    seq_13 = ['loot.ply']
    g_13 = [1.0, 1.0/64, 1.0/32, 1.0/16, 1.0/8, 1.0/4, 1.0/2]

    seq_12 = ['loot.ply']
    g_12 = [1.0, 1.0/32, 1.0/16, 1.0/8, 1.0/4, 1.0/2, 3.0/4]

    seq_11 = ['loot.ply']
    g_11 = [1.0, 1.0/16, 1.0/8, 1.0/4, 1.0/2, 3.0/4, 7.0/8]

    seq_10 = ['loot.ply']
    g_10 = [1.0, 1.0/8, 1.0/4, 1.0/2, 3.0/4, 7.0/8, 15.0/16]

    
    c = [4, 22, 28, 34, 40, 46, 51]

    cmd_all = []
    cmd_all.append(process_one_depth(gpcc_bin_path, ref_dir, cfg_dir, output_dir, seq_15, g_15, c))
    cmd_all.append(process_one_depth(gpcc_bin_path, ref_dir, cfg_dir, output_dir, seq_14, g_14, c))
    cmd_all.append(process_one_depth(gpcc_bin_path, ref_dir, cfg_dir, output_dir, seq_13, g_13, c))
    cmd_all.append(process_one_depth(gpcc_bin_path, ref_dir, cfg_dir, output_dir, seq_12, g_12, c))
    cmd_all.append(process_one_depth(gpcc_bin_path, ref_dir, cfg_dir, output_dir, seq_11, g_11, c))
    cmd_all.append(process_one_depth(gpcc_bin_path, ref_dir, cfg_dir, output_dir, seq_10, g_10, c))


    with open('run_gpcc_encode_new.sh', 'w') as f:
        for item in cmd_all:
            print(item)
            f.write('%s & \n' % item)
