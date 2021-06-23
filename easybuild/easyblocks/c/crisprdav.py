##
# Copyright 2020-2021 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# https://github.com/easybuilders/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for building and installing Metagenome-Atlas, implemented as an easyblock.

@author: Denis Kristak (INUITS)
"""
import os
from easybuild.tools.filetools import write_file
from easybuild.easyblocks.generic.binary import Binary


class EB_crisprdav(Binary):
    """
    Support for building/installing crispr-dav.
    """

    def post_install_step(self):
        """Create config.txt files"""
        crisprdav_installdir = self.installdir
        abra2_dir = os.environ['EBROOTABRA2']
        prinseq_dir = os.environ['EBROOTPRINSEQ']
        flash_dir = os.environ['EBROOTFLASH']

        config_file = os.path.join(self.installdir, 'conf.txt')
        example_fastq_list_file = os.path.join(self.installdir, 'Examples/example1/fastq.list')

        # writing to Example directory to run sanity checks
        example_config_file = os.path.join(self.installdir, 'Examples/example1/conf.txt')

        CONFIG_FILE_TEXT_FORMATTED = CONFIG_FILE_TEXT.format(crisprdav_installdir=crisprdav_installdir,
                                                             abra2_dir=abra2_dir, prinseq_dir=prinseq_dir,
                                                             flash_dir=flash_dir)
        FASTQ_LIST_FILE_TEXT_FORMATTED = FASTQ_LIST_FILE_TEXT.format(crisprdav_installdir=crisprdav_installdir)
        # according to docs, we have to setup conf.txt so that it contains correct paths to dependencies
        # https://github.com/pinetree1/crispr-dav/blob/master/Install-and-Run.md
        # User then has to change conf.txt to include paths to genomes
        write_file(config_file, CONFIG_FILE_TEXT_FORMATTED)
        write_file(example_config_file, CONFIG_FILE_TEXT_FORMATTED)
        # also used for sanity checking with Examples/ folder
        write_file(example_fastq_list_file, FASTQ_LIST_FILE_TEXT_FORMATTED)


# obtained from
# https://github.com/pinetree1/crispr-dav/blob/master/conf.txt
# see the original file for detailed commentary
CONFIG_FILE_TEXT = """
# change this part to contain paths to your genomes
[genomex]
ref_fasta = {crisprdav_installdir}/Examples/example1/genome/genomex.fa
bwa_idx = {crisprdav_installdir}/Examples/example1/genome/genomex.fa
refGene = {crisprdav_installdir}/Examples/example1/genome/refgenex.txt

[app]
abra = {abra2_dir}/abra2-2.23.jar
prinseq = {prinseq_dir}/prinseq-lite.pl
flash = {flash_dir}/bin/flash2

[prinseq]
min_qual_mean = 30
min_len	= 50
ns_max_p = 3

[other]
realign_flag = Y
min_mapq = 20
wing_length = 100
high_res = 0
parallel_env = orte
cores_per_job = 12
"""

FASTQ_LIST_FILE_TEXT = r"""
sample1	{crisprdav_installdir}/Examples/example1/rawfastq/sample1_R1.fastq.gz	{crisprdav_installdir}/Examples/example1/rawfastq/sample1_R2.fastq.gz
sample2	{crisprdav_installdir}/Examples/example1/rawfastq/sample2_R1.fastq.gz	{crisprdav_installdir}/Examples/example1/rawfastq/sample2_R2.fastq.gz
sample3	{crisprdav_installdir}/Examples/example1/rawfastq/sample3_R1.fastq.gz	{crisprdav_installdir}/Examples/example1/rawfastq/sample3_R2.fastq.gz
sample4	{crisprdav_installdir}/Examples/example1/rawfastq/sample4_R1.fastq.gz	{crisprdav_installdir}/Examples/example1/rawfastq/sample4_R2.fastq.gz
"""
