# The use of this file is to iterate through an index( I1 )
# group the names
# generate files
# go through R1, R2 and I2 and set in to different files

import pandas as pd
import gzip
import argparse

class fastapasta(object):


    def fasta_reader(self,file):
        """open .gz and normal files to python var """
        if file.endswith('gz'):
            f = gzip.open(file, 'rb')
        else:
            f = open(file, 'rb')
        return f

    def read4lines(self,f):
        """reads file in segments of four, f.ex fastq files"""
        line1 = f.readline()
        line2 = f.readline()
        line3 = f.readline()
        line4 = f.readline()
        return {'1': line1, '2': line2, '3': line3, '4': line4}

    def get_index(self, lines):
        """Get index from first line of file """
        try :
            sline1 = str(lines['1'])
            ixone = sline1.split(':')[9].split('+')[0]
            return ixone
        except IndexError:
            print(" line not correct, could be the last line of a test file ?")
            pass

    def read_csv(self, file_toread):
        """get csv index file (or any other files) as pandas df """
        index_file = pd.read_csv(file_toread)
        return index_file

    def index_pair(self, idf, ixone):
        """Matches index with indexfile"""
        try:
            idmatch = idf.loc[idf['index'] == ixone, 'Sample_Name'].values[0]
            return idmatch
        except IndexError:
            return 'undetermined'

    def write2file(self, direc, idmatch, lines):
        """write lines to file named after the idmatch in defined directory"""
        with open('{0}/{1}.fq'.format(direc,idmatch ), "ab+") as file:
            file.write(lines['1'])
            file.write(lines['2'])
            file.write(lines['3'])
            file.write(lines['4'])


def arguments():
    """Argument parser for data"""
    parser = argparse.ArgumentParser(description='give undetermined fastq file, samplesheet and a output directory ')

    parser.add_argument('-f', '--fastq', help='Input SVC', required=True)
    parser.add_argument('-id', '--indexfile', help='outfile here', required=True)
    parser.add_argument('-out', '--outdir', help='outfile here', required=True)

    args = vars(parser.parse_args())
    return args


def main(fp,file,indexfile,directory):
    fp = fp()
    f = fp.fasta_reader(file)
    idf = fp.read_csv(indexfile)
    while True:
        lines = fp.read4lines(f)
        index = fp.get_index(lines)
        idmatch = fp.index_pair(idf, index)
        fp.write2file(directory, idmatch, lines)
        if not lines['4']:
            break


if __name__ == '__main__':
    args = arguments()
    main(fastapasta,args['fastq'],args['indexfile'],args['outdir'])



