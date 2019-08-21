from datetime import datetime

def convert_to_vcard(input_file, input_file_format):
    
    FN = input_file_format['name']-1 if 'name' in input_file_format else None
    TEL = input_file_format['tel']-1 if 'tel' in input_file_format else None
    
    vcf_filename = 'vcard/contacts_' + str(datetime.now().strftime('%Y-%m-%d|%H:%M:%S')) + '.vcf'
    with open(vcf_filename, 'w') as single_vcf:
        for row in input_file:
            FN_VAL = row[FN] if FN is not None else ''
            TEL_VAL = str(row[TEL] if TEL is not None else '')
            
            print ('BEGIN:VCARD')
            print ('FN:' + FN_VAL)
            print ('TEL:' + TEL_VAL)
            print ('END:VCARD')
            print ('----------------------')
            single_vcf.write( 'BEGIN:VCARD' + "\n")            
            single_vcf.write( 'N:' + FN_VAL + ';' + "\n")
            single_vcf.write( 'FN:' + FN_VAL + "\n")            
            single_vcf.write( 'TEL;HOME;VOICE:' + TEL_VAL + "\n")           
            single_vcf.write( 'END:VCARD' + "\n")
            single_vcf.write( "\n")
    
    print("VCARDS Written")
    return vcf_filename
