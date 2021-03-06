################################################################################
#
#  NetFPGA-10G http://www.netfpga.org
#
#  File:
#        nf10_mdio_v2_1_0.tcl
#
#  Library:
#        sw/std/drivers/nf10_mdio_v1_00_a
#
#  Description:
#        Driver TCL script
#
#  Copyright notice:
#        Copyright (C) 2010, 2011 The Board of Trustees of The Leland Stanford
#                                 Junior University
#
#  Licence:
#        This file is part of the NetFPGA 10G development base package.
#
#        This file is free code: you can redistribute it and/or modify it under
#        the terms of the GNU Lesser General Public License version 2.1 as
#        published by the Free Software Foundation.
#
#        This package is distributed in the hope that it will be useful, but
#        WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#        Lesser General Public License for more details.
#
#        You should have received a copy of the GNU Lesser General Public
#        License along with the NetFPGA source package.  If not, see
#        http://www.gnu.org/licenses/.
#
#

proc generate {drv_handle} {
  xdefine_include_file $drv_handle "xparameters.h" "XEmacLite" "NUM_INSTANCES" "DEVICE_ID" "C_BASEADDR" "C_HIGHADDR" "C_TX_PING_PONG" "C_RX_PING_PONG" "C_INCLUDE_MDIO" "C_INCLUDE_INTERNAL_LOOPBACK"
  xdefine_config_file $drv_handle "xemaclite_g.c" "XEmacLite"  "DEVICE_ID" "C_BASEADDR" "C_TX_PING_PONG" "C_RX_PING_PONG" "C_INCLUDE_MDIO" "C_INCLUDE_INTERNAL_LOOPBACK"

  xdefine_canonical_xpars $drv_handle "xparameters.h" "EmacLite" "DEVICE_ID" "C_BASEADDR" "C_HIGHADDR" "C_TX_PING_PONG" "C_RX_PING_PONG" "C_INCLUDE_MDIO" "C_INCLUDE_INTERNAL_LOOPBACK"
}
