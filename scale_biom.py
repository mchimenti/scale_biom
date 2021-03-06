import argparse

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def scale_abundance(biom_element):    
    for i, element in enumerate(biom_element):
        if is_number(element.strip(']')) == True and float(element.strip(']')) != 1 and float(element.strip(']')) != 0:
            biom_element[i] = str(int(float(element.strip(']'))*1000000)) + ']'  #return string of integer value after multiplication
            print "Converting ", element, " to ", biom_element[i]
        else:
            continue
    return biom_element


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description=
        "This program is designed to scale a BIOM file from MetaPhlan2 \
        that has relative abundances, and convert to integer 'counts' on a per million basis"
        )
        
    parser.add_argument('filename', type=str, nargs = 1, help='the BIOM file to process')
    
    args = parser.parse_args()
    
    with open(args.filename[0], "r") as f:
        biom = f.readlines()
    
    biom_element = biom[0].strip().split(',')  #the whole BIOM file is one line with no newlines
    scaled_biom_element = scale_abundance(biom_element)
    scaled_biom = (',').join(scaled_biom_element)  
    scaled_biom = scaled_biom.replace('],"rows":', ']],"rows":')  #format back to valid JSON
    scaled_biom = scaled_biom.replace('"type": null', '"type":"OTU table"') #format for R/Phyloseq

    with open("scaled_" + args.filename[0], "w") as g:
        g.write(scaled_biom)
        g.write('\n')                                             #format back to valid JSON
        

