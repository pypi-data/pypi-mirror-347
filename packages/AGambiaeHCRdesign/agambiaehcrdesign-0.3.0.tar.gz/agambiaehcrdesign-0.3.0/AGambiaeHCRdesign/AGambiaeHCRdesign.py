import sys
from subprocess import Popen, PIPE
import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils import GC, MeltingTemp




def read_fasta(file_path): # Renamed to indicate it's more robust
    """
    Reads the first record from a FASTA file with error handling.

    Args:
        file_path (str): The path to the FASTA file.

    Returns:
        tuple: (ID, description, sequence) if successful.
               (None, None, None) if an error occurs (e.g., file not found,
               wrong format, or no records).
    """
    try:
        # Attempt to parse the file
        # SeqIO.parse returns a generator. We convert it to a list
        # to easily check if it's empty and access the first element.
        records = list(SeqIO.parse(file_path, 'fasta'))

        if not records:
            # This means the file was parseable as FASTA (or at least didn't immediately error),
            # but contained no records.
            print(f"Error: No FASTA records found in '{file_path}'. The file might be empty.", file=sys.stderr)
            return None, None, None

        # Get the first record
        first_record = records[0]
        ID = first_record.id
        desc = first_record.description
        sequence = first_record.seq

        print('Transcript ID: ', ID)
        print('Transcript Description: ',desc)
        print('Transcript Sequence: ',sequence)

        return ID, desc, sequence

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        return None, None, None
    except ValueError as e:
        # Biopython's SeqIO.parse raises ValueError for format issues.
        # This can happen if the file is not FASTA or is malformed.
        # The error message from Biopython can be quite informative.
        print(f"Error: Could not parse '{file_path}' as FASTA. It might be the wrong format or corrupted. Details: {e}", file=sys.stderr)
        return None, None, None
    except Exception as e:
        # Catch any other unexpected errors during file processing
        print(f"An unexpected error occurred while processing '{file_path}': {e}", file=sys.stderr)
        return None, None, None



#function to create oligo pairs from input sequence
def create_oligos(sequence,oligo_length=25,gap_length=2,frame_start_position=0):
    """
    This function designs a set of forward and reverse oligos from an input sequence,
    with added error handling.

    Args:
        sequence (str): The input nucleotide sequence.
        oligo_length (int, optional): The length of each oligo. Defaults to 25.
        gap_length (int, optional): The gap between the forward and reverse oligo. Defaults to 2.
        frame_start_position (int, optional): The starting position for the first oligo. Defaults to 0.

    Returns:
        list: A list of SeqRecord objects representing the generated oligos.
              Returns an empty list if no oligos could be generated.
    """

    if not isinstance(oligo_length, int) or not isinstance(gap_length, int) or not isinstance(frame_start_position, int):
        raise TypeError("Oligo length, gap length, and frame start position must be integers.")

    # Input value validation
    if oligo_length <= 0:
        raise ValueError("Oligo length must be a positive integer.")
    if gap_length < 0:
        raise ValueError("Gap length must be a non-negative integer.")
    if frame_start_position < 0 or frame_start_position >= len(sequence):
        raise ValueError("Frame start position is out of range.")



    n = frame_start_position
    ol = oligo_length
    gl = gap_length
    k = frame_start_position + ol + gl; #start position for odd probes; using 20 nt oligo pairs
    j = len(sequence) #sequence length
    
    oligos_all=[]
    
    for idx,i in enumerate(range(j)):
        if (k+ol-gl)<=j: #if length of even+odd is smaller than length of trunacted sequence
            e_rna = sequence[n:n+ol] #even rna seq object 20 nt in length
            o_rna = sequence[k:k+ol] #odd ran seq object 20 nt in length
            EV = e_rna.reverse_complement() #reverse complement both
            OD = o_rna.reverse_complement()
            oligos_all.append(EV) #append the tag to seq
            oligos_all.append(OD) #append seq to tag
            n=n+((ol+gl)*2) #increment starting position to even oligo to new position with gap
            k=k+((ol+gl)*2) #increment starting position of odd oligo to new position with gap

    print('Oligos tiled along the transcript sequence: \n')
    print(oligos_all)
            
    return oligos_all


def adjacency_filter(dframe):
    dataset = dframe.copy()
    
    uqids = dataset.qid.unique() #get unique query IDs
    
    
    j = -1 
    for i in range(len(uqids)-1):
        if not (uqids[i]-j==1 or uqids[i+1]-uqids[i]==1):
            indexNames = dataset[dataset['qid'] == uqids[i]].index
            dataset.drop(indexNames, inplace=True)
        j = uqids[i]

    if uqids[-1]-uqids[-2] != 1:
        indexNames = dataset[dataset['qid'] == uqids[-1]].index
        dataset.drop(indexNames, inplace=True)
            
    return dataset



def blast_oligos(oligos_all, dbname):

    records = []

    for (index, sequence) in enumerate(oligos_all):
        records.append(SeqRecord(sequence, id=str(index+1)))
    
    SeqIO.write(records,'oligos.faa','fasta')
    
    cmd_list = ['blastn', '-db', dbname, '-query', 'oligos.faa', '-outfmt', '6', '-out', 'result_tab.txt', '-task', 'blastn-short', '-evalue', '100', '-strand', 'minus']
    print('Running batch BLAST on oligos')
    blast_process = Popen(cmd_list, stdout=PIPE, stderr=PIPE) #run command
    return_code = blast_process.wait() #wait for blast to finish

    if return_code != 0:
        raise IOError("BLAST Error! BLAST is not configured correctly") #error handling to display error code specifically related to BLAST+ exes
        err = blast_process.stderr.read() #read error from BLAST
        print(err)
    
    elif return_code == 0:
        print('BLAST completed successfully')
        out = blast_process.stdout.read() #read output from BLAST

    blast_result = pd.read_csv('result_tab.txt', sep="\t", header=None, 
                       names=['qid','sseqid','pident','length','mismatch','gapopen','qstart','qend','sstart','send','evalue','bitscore'],
                        index_col=None)

    return blast_result  


def filter_and_rank(ID, oligos_all, blast_result, GC_range=[37,85], Tm_range=[47,85]):

    data = blast_result.loc[~blast_result['sseqid'].str.startswith(ID[:10])]
    data_filtered = data.loc[data['length']>0.6*data['length'].max()] #filter by hit length >60% of seq length

    data_new = data_filtered.copy()

    print('Filtering out oligos based on GC content and Melting Temperature...')

    GCcon = [] 
    MT = []
    #calculate GC content and Melting temp for each oligo
    for oligo in oligos_all:
        tempgc = GC(oligo)
        tempmt = MeltingTemp.Tm_GC(oligo,strict=False)
        GCcon.append(tempgc)
        MT.append(tempmt)

    #filter by GC content and annealing temp 
    for idx,gc in enumerate(GCcon):
        if ((gc<=GC_range[0] or gc>=GC_range[1]) or (MT[idx]<=Tm_range[0] or MT[idx]>=Tm_range[1])): #gc-range 37-85 MT-range 53-85
            indexNames = data_new[data_new['qid'] == idx].index
            data_new.drop(indexNames, inplace=True)
    
    #filter for missing adjacent pairs
    data_new = adjacency_filter(data_new)
    print('Filtering Completed')


    print('Filtering out oligos if adjacent oligos have hits on the same transcript...')
    uqids = data_new.qid.unique()

    i = 0
    while i<len(uqids)-1:
        if uqids[i+1]-uqids[i] == 1:
            temp1 = data_new.loc[data_new['qid'] == uqids[i],'sseqid']
            temp2 = data_new.loc[data_new['qid'] == uqids[i+1],'sseqid']
            match = set(temp1) & set(temp2)

            if len(match)>1:
                indexNames = data_new[data_new['qid'] == uqids[i]].index
                data_new.drop(indexNames, inplace=True)
                indexNames = data_new[data_new['qid'] == uqids[i+1]].index
                data_new.drop(indexNames, inplace=True)
                i=i+2
            else:
                i=i+1
        else:
            i=i+1
            
    data_new = adjacency_filter(data_new)
    print('Fitering Completed')

    uqids = data_new.qid.unique()

    #rank each oligo by number of unique geneid hits and then rank pairs by average no. of hits between them
    print('Ranking oligo pairs by specificity')

    score = []
    for ids in uqids:
        temp = data_new.loc[data_new['qid'] == ids,'sseqid']
        temp_score = len(temp.unique())
        score.append(temp_score)
        
    
    avg_score = []
    oligos1 = []
    oligos2 = []
    oligo1seq = []
    oligo2seq = []


    i = 0
    while i<len(uqids)-1:
        if uqids[i+1]-uqids[i] == 1:
            temp_score = (score[i]+score[i+1])/2
            avg_score.append(temp_score)
            temp1 = uqids[i]
            temp2 = uqids[i+1]
            oligos1.append(temp1)
            oligos2.append(temp2)
            tempseq1 = oligos_all[uqids[i]-1] 
            tempseq2 = oligos_all[uqids[i]]
            oligo1seq.append(str(tempseq1))
            oligo2seq.append(str(tempseq2))
            i=i+1
        else:
            i=i+1
    

    print('Ranking Completed')

    #create new dataframe with best possible pairs
    d = {'Oligo1_Position': oligos1, 'Oligo2_Position': oligos2, 'Oligo1_Sequence': oligo1seq, 'Oligo2_Sequence': oligo2seq, 'Score (average hits)': avg_score}
    datasheet = pd.DataFrame(data=d)
    
    datasheet = datasheet.sort_values(by=['Score (average hits)'])
    datasheet = datasheet.reset_index()
    datasheet = datasheet.drop(['index'],axis=1)
    
    s1 = list(pd.Series(datasheet['Oligo1_Position'].values))
    s2 = list(pd.Series(datasheet['Oligo2_Position'].values))
    scores = list(pd.Series(datasheet['Score (average hits)'].values))
    match = (set(s1)&set(s2))
    
    #maximize adjacent pairs for best scores, that are not overlapping
    k = 0
    indexNames = []
    s1_temp = s1.copy()
    s2_temp = s2.copy()
    while len(match)>0:
        if s2[k] in s1:
            tempi = s1.index(s2[k])
            if (s2[k] in s1_temp and s2[k] in s2_temp):
                if scores[k]<=scores[tempi]:
                    i = s1_temp.index(s1[tempi])
                    del s1_temp[i]
                    del s2_temp[i]
                    indexNames.append(tempi)
                else:
                    i = s2_temp.index(s2[k])
                    del s1_temp[i]
                    del s2_temp[i]
                    indexNames.append(k)
            
        k=k+1
        match = (set(s1_temp)&set(s2_temp))
        
    #remove pairs according to maximization
    datasheet.drop(indexNames,inplace=True)
    datasheet = datasheet.reset_index()
    probe_datasheet = datasheet.drop(['index'],axis=1)
    
    npairs = len(datasheet['Oligo1_Position'])
    print('Generated number of optimized HCR probe pairs: ', npairs)

    return probe_datasheet



def add_hairpin(probe_datasheet, hairpin):
    """
    Generates HCR probes by adding hairpin sequences to the input sequences.

    Args:
        probe_datasheet (dict): A dictionary containing probe information, including
            'Sequence1' and 'Sequence2' lists.  It is assumed that the dictionary
            is already populated with these keys, and that the values are lists
            of DNA sequences (strings).
        hairpin (str): A string indicating the hairpin type ('B1', 'B2', 'B3', 'B4', or 'B5').

    Returns:
        dict: A modified dictionary with two new keys, 'oligoseq1' and 'oligoseq2',
            containing the modified sequences with added hairpin sequences.
            Returns the original dictionary if the hairpin type is invalid.
    """
    print('Generating HCR probes...')

    # Define hairpin sequences.  Use a dictionary for efficient lookup.
    hairpin_sequences = {
        'B1': ('gAggAgggCAgCAAACggAA', 'TAgAAgAgTCTTCCTTTACg'),
        'B2': ('CCTCgTAAATCCTCATCAAA', 'AAATCATCCAgTAAACCgCC'),
        'B3': ('gTCCCTgCCTCTATATCTTT', 'TTCCACTCAACTTTAACCCg'),
        'B4': ('CCTCAACCTACCTCCAACAA', 'ATTCTCACCATATTCgCTTC'),
        'B5': ('CTCACTCCCAATCTCTATAA', 'AACTACCCTACAAATCCAAT'),
    }

    # Check if the hairpin type is valid.
    if hairpin not in hairpin_sequences:
        print(f"Error: Invalid hairpin type '{hairpin}'.  Returning original data.")
        return probe_datasheet  # Important: Return original data on error

    I_even, I_odd = hairpin_sequences[hairpin]  # Get sequences from dictionary

    # Process 'Sequence1'
    oligos1seq = probe_datasheet.get('Oligo1_Sequence', []) #handles the key error. returns empty list if not found
    oligos1_hp = [I_even.upper() + seq for seq in oligos1seq]  # List comprehension

    # Process 'Sequence2'
    oligos2seq = probe_datasheet.get('Oligo2_Sequence', []) #handles the key error. returns empty list if not found
    oligos2_hp = [seq + I_odd.upper() for seq in oligos2seq]  # List comprehension

    # Update the dictionary.  Always create the new keys.
    probe_datasheet['HCRprobe1'] = oligos1_hp
    probe_datasheet['HCRprobe2'] = oligos2_hp

    print('HCR probes designed')
    return probe_datasheet
    
    

    