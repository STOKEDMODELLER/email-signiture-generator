import pandas as pd
from segno import helpers
import base64
from cairosvg import svg2png
import os
import numpy as np
from os import path

if not os.path.exists('QR'):
    os.makedirs('QR')
if not os.path.exists('signitures'):
    os.makedirs('signitures')
if not os.path.exists('signitures_png'):
    os.makedirs('signitures_png')
    
dirToQR = 'QR/'
signitures = 'signitures/'
signitures_png = 'signitures_png/'



def vcard(data,dirToQR):
    qr = helpers.make_vcard(name=data['surname']+';'+data['firstname'],
                            displayname=data['firstname']+' '+data['surname'],
                            email=data['email'],
                            phone=(data['cell'],data['phone']),
                            fax = data['fax'],
                            title =data['qualification'],
                            street=data['Address'],
                            pobox=data['Postal'],
                            url='www.mbb.co.za'
                            )
    qr.designator
    qr.save('{}.svg'.format(dirToQR+data['email']), scale=4)
    qr.save('{}.png'.format(dirToQR+data['email']), scale=4)

def generate_signiture(data,dirToQR,signitures):
    encoded = base64.b64encode(open(dirToQR+data['email']+'.png', "rb").read())
    dir_name = signitures+data['email']
    dir_name_png = signitures_png+data['email']
    # data = filename_img
    
    create_svg(dir_name_png,dir_name,data)
    data = [data['email'],
             data['cell'],
             data['phone'],
             data['jobtitle'],
             data['firstname']+' '+data['surname'],
             data['qualification'],
             data['organisation'],
             data['fax'],
             'data:image/png;base64,'+encoded.decode("utf-8")
             ] 
    data1 = ['email','cell','tel11','title1','full_name','qualll','branch','fax','filename_image']
    generator(data1,data,dir_name)
    
    
def generator(data1,data,dir_name,dir_name_png):
    import os.path
    
    if os.path.isfile('{}.svg'.format(dir_name)):
        os.remove('{}.svg'.format(dir_name))
        open('{}.svg'.format(dir_name), 'a').write(open('Template_R01.svg', 'r').read())
        for i,c in enumerate(data1):
            # Read in the file
            with open('{}.svg'.format(dir_name), 'r') as file :
              filedata = file.read()
            # print(c,data[i])
            # Replace the target string
            filedata = filedata.replace(c,data[i])
            # Write the file out again
            with open('{}.svg'.format(dir_name), 'w') as file:
              file.write(filedata)
    
    else:
        open('{}.svg'.format(dir_name), 'a').write(open('Template_R02.svg', 'r').read())
        for i,c in enumerate(data1):
            # Read in the file
            with open('{}.svg'.format(dir_name), 'r') as file :
              filedata = file.read()
            # print(c,data[i])
            # Replace the target string
            filedata = filedata.replace(c,data[i])
            # Write the file out again
            with open('{}.svg'.format(dir_name), 'w') as file:
              file.write(filedata)
              
def png_maker(dir_name,dir_name_png):
    if os.path.isfile('{}.png'.format(dir_name_png)):
        os.remove('{}.png'.format(dir_name_png))
        svg2png(bytestring=open("{}.svg".format(dir_name),"r", encoding='utf8').read(),write_to=open('{}.png'.format(dir_name_png),'wb'),dpi=1080)
    else:
        try:
            svg2png(bytestring=open("{}.svg".format(dir_name),"r", encoding='utf8').read(), write_to=open('{}.png'.format(dir_name_png),'wb'),dpi=1080)

        except:
            svg2png(bytestring=open("{}.svg".format(dir_name),"r", encoding='ISO-8859-1').read(), write_to=open('{}.png'.format(dir_name_png),'wb'),dpi=1080)

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

        
d = pd.read_csv('MBB_Services_International-Senders.csv', encoding = "ISO-8859-1").fillna('')


printProgressBar(0, d.shape[0], prefix = 'Progress:', suffix = 'Complete', length = 50)

for i in range(d.shape[0]):
    branch = d.iloc[i]['branch']
    email = d.iloc[i]['email']
    firstname = d.iloc[i]['firstname']
    surname = d.iloc[i]['surname']
    jobtitle = d.iloc[i]['jobtitle']
    phone = d.iloc[i]['phone']
    cell = d.iloc[i]['cell']
    fax = d.iloc[i]['fax']
    qualification = d.iloc[i]['qualification']
    organisation = d.iloc[i]['organisation']
    addr = d.iloc[i]['Address']
    pobox = d.iloc[i]['Postal']
    
    data1= {'branch':branch,
           'email':email,
           'firstname':firstname,
           'surname':surname,
           'jobtitle':jobtitle,
           'phone':phone,
           'cell':cell,
           'fax':fax,
           'qualification':qualification,
           'organisation':organisation,
           'Address':addr,
           'Postal':pobox
        }
    vcard(data1,dirToQR)
    data = d.iloc[i]
    dir_name =signitures+data['email']
    dir_name_png = signitures_png+data['email']
    encoded = base64.b64encode(open(dirToQR+data['email']+'.png', "rb").read())
    data = [data['email'],
             data['cell'],
             data['phone'],
             data['jobtitle'],
             data['firstname']+' '+data['surname'],
             data['qualification'],
             data['organisation'],
             data['fax'],
             '"data:image/png;base64,'+encoded.decode("utf-8")+'"',
             data['Address']
             
             ] 
    data1 = ['email','cell','tel11','title1','full_name','qualll','branch','fax','filename_image','addr']
    generator(data1,data,dir_name,dir_name_png)
    png_maker(dir_name,dir_name_png)
    # print(str(np.round(i*100/d.shape[0]))+'%')
    printProgressBar(i + 1, d.shape[0], prefix = 'Progress:', suffix = 'Complete', length = 50)