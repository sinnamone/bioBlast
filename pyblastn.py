import subprocess
from Bio.Blast.Applications import NcbiblastnCommandline
import optparse
import sys 
import os

parser = optparse.OptionParser(usage='python %prog ',version='1.0',)
parser.add_option('-f', action="store", dest="fastaref",help='Fasta file for makeblastdb',default=None)
parser.add_option('-i', action="store", dest="fastatarget",help='Multi Fasta file for to perferm Blastn')
parser.add_option('-o', action="store", dest="output",help='Output Id',default = None)
parser.add_option('-p', action="store", dest="pathout",help='Output Pathway', default = None)
options, args = parser.parse_args()


class makeblastdatabase(object):
	def __init__(self,fastaref,outid,pathout):
		self.FNULL = open(os.devnull, 'w')
		self.fastaref=fastaref
		self.outid = outid
		self.dbid = os.path.basename(fastaref.split('/')[-1]) 
		if pathout.endswith('/') == True:
			self.path_out = pathout
		else:
			self.path_out = pathout+'/'	
	
	def makeblast(self):
		try:
			if os.path.isfile(self.path_out + self.dbid+'.db' ) is False :
				print ('Preparing make blast db.')
				subprocess.check_call(['makeblastdb','-in',self.fastaref,'-dbtype','nucl','-out', self.path_out + self.dbid+'.db'],stderr = self.FNULL,stdout = self.FNULL )
			else:
				sys.stdout.write('Database already exist. Exit\n')
		except subprocess.CalledProcessError:
			sys.stdout.write('Error makeblastdb. Exit\n')
			sys.exit(0)
		else:
			sys.stdout.write('Make blast db complete.\n')

		
class blastnlucleotide(makeblastdatabase):
	def __init__(self,fastaref,input,outid,pathout):
		makeblastdatabase.__init__(self,fastaref,outid,pathout)
		self.input = input
	
	def blastn(self):
		try:
			
			subprocess.check_call(['blastn','-out',self.path_out+self.outid+'_blastn.tab','-outfmt','7','-query',self.path_out+self.outid+'.fasta','-db', self.fastaref+'.db','-evalue','0.001','-num_threads','2'],stderr = self.FNULL,stdout = self.FNULL)
		except:
			sys.stdout.write('Error during blastn analysis. Exit\n')
			sys.exit(0)	
		else:
			sys.stdout.write('Blastn analysis complete.\n')

		
if __name__ == '__main__':
		print ('Blastn starting analysis.')
		a = blastnlucleotide(fastaref=options.fastaref,input=options.fastatarget,outid=options.output,pathout=options.pathout).makeblast()
		a = blastnlucleotide(fastaref=options.fastaref,input=options.fastatarget,outid=options.output,pathout=options.pathout).blastn()
