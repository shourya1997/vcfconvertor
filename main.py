import query_and_write as qw
import vcfconvert
import select_and_hash as sh
import time

if __name__ == "__main__":
    '''
    1. Query database to get results
    2. Write results in file
    3. Select last/latest 2 files in directory and create MD5 of both respectively
    4. If MD5 different then create VCF of latest file created
        4.1 Upload VCF in S3 bucket
        4.2 Send this VCF file through email
    5. If MD5 same then don't create VCF
    '''
    
    result = qw.query_return()
    result_file_path = qw.result_to_file(result)

    if sh.hash_compare():
        # convert to vcf
        input_format = qw.input_format
        vcf_filename = vcfconvert.convert_to_vcard(result, input_format)

        upload_old = qw.upload_to_aws(vcf_filename, vcf_filename)
        
        s3_filename = 'myoperator_numbers.vcf'
        
        uploaded = qw.upload_to_aws(vcf_filename, s3_filename)
        
        if uploaded:
            message = "MyOperator VCard has been Update for the following date:" + str(time.strftime("%Y-%m-%d %H:%M:%S"), time.localtime()) + "(IST). Please download it from the link shared."
            qw.send_email(message)
        else:
            pass

    else:
        print("No Update in Contacts")