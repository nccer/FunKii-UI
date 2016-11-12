
try: #Python 2 imports
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
    from HTMLParser import HTMLParser
    
except ImportError: #Python 3 imports
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog
    from html.parser import HTMLParser

import os    
import FunKiiU as fnku
import json
import zipfile
from AutoComplete import AutocompleteCombobox
from distutils.version import LooseVersion

urlopen=fnku.urlopen
URLError=fnku.URLError
HTTPError=fnku.HTTPError
PhotoImage=tk.PhotoImage

__VERSION__="2.1"
targetversion="FunKiiU v2.2"
current_gui=LooseVersion(__VERSION__)
### I'm getting about 80 titles not parsing from titlekeys.json
### properly. To see the error output, set DEBUG = True. The
### parsing code is found in load_title_data beginning on line 337.

DEBUG = False

if os.name == 'nt':
    dir_slash = "\\"
else:
    dir_slash = "/"
try:
    fnku_VERSION_ = str(fnku.__VERSION__)
    current_fnku=LooseVersion(fnku_VERSION_)
except:
    fnku.__VERSION__ = "?"
    current_fnku=LooseVersion('0')




class VersionParser(HTMLParser):
    fnku_data_set=[]
    gui_data_set=[]
    
    def handle_starttag(self, tag, attrs):
        fnku_data_set=[]
        gui_data_set=[]
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    if value.startswith("/llakssz") and value.endswith(".zip"):
                        self.fnku_data_set.append(value)
                    elif value.startswith("/dojafoja") and value.endswith(".zip"):
                        self.gui_data_set.append(value)

                
class RootWindow(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self)
        self.versions={'gui_new':'','gui_all':'','gui_url':'https://github.com/dojafoja/FunKii-UI/releases','fnku_new':'','fnku_all':'',
                       'fnku_url':'https://github.com/llakssz/FunKiiU/releases'}

        self.download_list=[]
        self.selection_list=[]
        self.title_data=[]
        self.nb = ttk.Notebook(self)
        tab1 = ttk.Frame(self.nb)
        self.tab2 = ttk.Frame(self.nb)
        tab3 = ttk.Frame(self.nb)
        tab4 = ttk.Frame(self.nb)
        self.nb.add(tab1,text="Welcome")
        self.nb.add(self.tab2,text="Download")
        self.nb.add(tab3,text="Options")
        self.nb.add(tab4,text="Updates")
        self.nb.pack(fill="both", expand=True)
        self.output_dir=tk.StringVar()
        self.retry_count=tk.IntVar(value=3)
        self.patch_demo=tk.BooleanVar(value=True)
        self.patch_dlc=tk.BooleanVar(value=True)
        self.tickets_only=tk.BooleanVar(value=False)
        self.simulate_mode=tk.BooleanVar(value=False)
        self.region_usa=tk.BooleanVar(value=False)
        self.region_eur=tk.BooleanVar(value=False)
        self.region_jpn=tk.BooleanVar(value=False)
        self.filter_usa=tk.BooleanVar(value=True)
        self.filter_eur=tk.BooleanVar(value=True)
        self.filter_jpn=tk.BooleanVar(value=True)
        self.filter_game=tk.BooleanVar(value=True)
        self.filter_dlc=tk.BooleanVar(value=True)
        self.filter_update=tk.BooleanVar(value=True)
        self.usa_selections={'game':[],'dlc':[],'update':[]}
        self.eur_selections={'game':[],'dlc':[],'update':[]}
        self.jpn_selections={'game':[],'dlc':[],'update':[]}
        self.errors=0
        

        # Tab 1
        t1_frm1=ttk.Frame(tab1)   
        t1_frm2=ttk.Frame(tab1)
        t1_frm3=ttk.Frame(tab1)
        t1_frm4=ttk.Frame(tab1)
        t1_frm5=ttk.Frame(tab1)
        t1_frm6=ttk.Frame(tab1)
        
        self.img = PhotoImage(file='logo.gif')
        logo=ttk.Label(t1_frm1,image=self.img).pack()
        lbl=ttk.Label(t1_frm2,justify='center',text='This is a simple GUI by dojafoja that was written for FunKiiU.\nCredits to cearp for writing FunKiiU and cerea1killer for rewriting\n it in way that made writing a GUI much easier.').pack()
        lbl=ttk.Label(t1_frm3,justify='center',text='If you plan on using an online methond to obtain keys or tickets\n then FunKiiU will need to know the name of *that key site*. If you\nhaven\'t already provided the address to the key site, you MUST do so\nbelow before proceeding. You only need to provide this information once!').pack(pady=15)
        self.enterkeysite_lbl=ttk.Label(t1_frm4,text='Enter the name of *that key site*. Something like wiiu.thatkeysite.com')
        self.enterkeysite_lbl.pack(pady=15,side='left')
        self.http_lbl=ttk.Label(t1_frm5,text='http://')
        self.http_lbl.pack(pady=15,side='left')
        self.keysite_box=ttk.Entry(t1_frm5,width=40)
        self.keysite_box.pack(pady=15,side='left')
        self.submitkeysite_btn=ttk.Button(t1_frm6,text='submit',command=self.submit_key_site)
        self.submitkeysite_btn.pack()
        self.updatelabel=ttk.Label(t1_frm6,text='')
        self.updatelabel.pack(pady=15)
        
        t1_frm1.pack()
        t1_frm2.pack()
        t1_frm3.pack()
        t1_frm4.pack()
        t1_frm5.pack()
        t1_frm6.pack()

        self.load_program_revisions()
        self.check_config_keysite()
        
        # Tab2
        t2_frm0=ttk.Frame(self.tab2)
        t2_frm1=ttk.Frame(self.tab2)
        t2_frm2=ttk.Frame(self.tab2)   
        t2_frm3=ttk.Frame(self.tab2)
        t2_frm4=ttk.Frame(self.tab2)
        t2_frm5=ttk.Frame(self.tab2)
        t2_frm6=ttk.Frame(self.tab2)
        t2_frm7=ttk.Frame(self.tab2)
        t2_frm8=ttk.Frame(self.tab2)
        t2_frm9=ttk.Frame(self.tab2)
        
        lbl=ttk.Label(t2_frm0,text='Enter as many Title ID\'s as you would like to the list. Entering a key is optional and only needed if you are NOT using\nthe online keys or online tickets method. If you are NOT using one of the online methods, then you must provide\na key for every title you add to the list or it will fail. Use the selection box to make life easier, however, it may not be a\ncomplete list of titles. You can still enter title ID and key manually. P.S. the selection box has auto-complete').pack(padx=5,pady=7)
        lbl=ttk.Label(t2_frm1,text='Choose regions to display:').pack(padx=5,pady=5,side='left')
        filter_box_usa=ttk.Checkbutton(t2_frm1,text='USA',variable=self.filter_usa,command=lambda:self.populate_selection_box(download_data=False)).pack(padx=5,pady=5,side='left')
        filter_box_eur=ttk.Checkbutton(t2_frm1,text='EUR',variable=self.filter_eur,command=lambda:self.populate_selection_box(download_data=False)).pack(padx=5,pady=5,side='left')
        filter_box_jpn=ttk.Checkbutton(t2_frm1,text='JPN',variable=self.filter_jpn,command=lambda:self.populate_selection_box(download_data=False)).pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t2_frm2,text='Choose content to display:').pack(padx=5,pady=5,side='left')
        filter_box_usa=ttk.Checkbutton(t2_frm2,text='Game',variable=self.filter_game,command=lambda:self.populate_selection_box(download_data=False)).pack(padx=5,pady=5,side='left')
        filter_box_eur=ttk.Checkbutton(t2_frm2,text='Update',variable=self.filter_update,command=lambda:self.populate_selection_box(download_data=False)).pack(padx=5,pady=5,side='left')
        filter_box_jpn=ttk.Checkbutton(t2_frm2,text='DLC',variable=self.filter_dlc,command=lambda:self.populate_selection_box(download_data=False)).pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t2_frm3,text='Selection:').pack(padx=5,pady=7,side='left')
        self.selection_box=AutocompleteCombobox(t2_frm3,values=(self.selection_list),width=73)
        self.selection_box.bind('<<ComboboxSelected>>', self.selection_box_changed)
        self.selection_box.bind('<Return>', self.selection_box_changed)
        self.selection_box.bind('<<NoHits>>', self.clear_id_key_boxes)
        
        self.selection_box.pack(padx=5,pady=7,side='left')
        btn=ttk.Button(t2_frm3,text='refresh',width=8,command=self.populate_selection_box).pack(side='left')
        lbl=ttk.Label(t2_frm4,text='Title ID:').pack(padx=5,pady=7,side='left')
        self.id_box=ttk.Entry(t2_frm4,width=40)
        self.id_box.pack(padx=5,pady=5,side='left')
        btn=ttk.Button(t2_frm4,text='Add to list',command=self.add_to_list).pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t2_frm5,text='Key:').pack(padx=5,pady=7,side='left')
        self.key_box=ttk.Entry(t2_frm5,width=40)
        self.key_box.pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t2_frm6,text='Download list:').pack()
        lbl=ttk.Label(t2_frm6,text='Items marked with ** have an entered key provided').pack()
        dl_scroller=ttk.Scrollbar(t2_frm6,orient='vertical')
        dl_scroller.pack(side='right',fill='y')
        self.dl_listbox=tk.Listbox(t2_frm6,width=73,height=12)
        self.dl_listbox.pack(fill='y')
        self.dl_listbox.config(yscrollcommand=dl_scroller.set)
        dl_scroller.config(command=self.dl_listbox.yview)
        btn=ttk.Button(t2_frm7,text='Remove selected',command=self.remove_from_list).pack(padx=3,pady=20,side='left',anchor='w')
        btn=ttk.Button(t2_frm7,text='Clear list',command=self.clear_list).pack(padx=3,pady=20,side='left')
        lbl=ttk.Label(t2_frm8,text='Add an entry to the download list one at a time.\nWhen you are done, click on a download button\nbelow based on your preferred method. Don\'t\nforget to visit the options tab before you\ndownload.').pack(padx=20,pady=10)
        btn=ttk.Button(t2_frm9,text='Download using online tickets',width=30,command=lambda:self.download_clicked(1)).pack(padx=5,pady=10,side='left')
        btn=ttk.Button(t2_frm9,text='Download using online keys',width=30,command=lambda:self.download_clicked(2)).pack(padx=5,pady=10,side='left')
        btn=ttk.Button(t2_frm9,text='Download using entered keys',width=30,command=lambda:self.download_clicked(3)).pack(padx=5,pady=10,side='left')

        self.populate_selection_box(download_data=False)
        
        t2_frm0.grid(row=0,column=1,columnspan=3,sticky='w')
        t2_frm1.grid(row=1,column=1,sticky='w')
        t2_frm2.grid(row=2,column=1,sticky='w')
        t2_frm3.grid(row=3,column=1,columnspan=3,sticky='w')
        t2_frm4.grid(row=4,column=1,sticky='w')
        t2_frm5.grid(row=5,column=1,sticky='w')
        t2_frm6.grid(row=6,column=2,rowspan=3,columnspan=2,padx=5,sticky='e')
        t2_frm7.grid(row=9,column=3,sticky='e')
        t2_frm8.grid(row=6,column=1,sticky='w')
        t2_frm9.grid(row=10,column=1,columnspan=3)
        
        # Tab3
        t3_frm1=ttk.Frame(tab3)
        t3_frm2=ttk.Frame(tab3)
        t3_frm3=ttk.Frame(tab3)
        t3_frm4=ttk.Frame(tab3)
        t3_frm5=ttk.Frame(tab3)
        t3_frm6=ttk.Frame(tab3)
        t3_frm7=ttk.Frame(tab3)
        t3_frm8=ttk.Frame(tab3)
        
        lbl=ttk.Label(t3_frm1,text='To use the default output directory, leave the entry blank').pack(padx=5,pady=10,side='left')
        lbl=ttk.Label(t3_frm2,text='Output directory').pack(padx=5,pady=5,side='left')
        self.out_dir_box=ttk.Entry(t3_frm2,width=35,textvariable=self.output_dir)
        self.out_dir_box.pack(padx=5,pady=5,side='left')
        btn=ttk.Button(t3_frm2,text='Browse',command=self.get_output_directory).pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t3_frm3,text='Retry count:').pack(padx=5,pady=5,side='left')
        self.retry_count_box=ttk.Combobox(t3_frm3,state='readonly',width=5,values=range(10),textvariable=self.retry_count)
        self.retry_count_box.set(3)
        self.retry_count_box.pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t3_frm4,text='Patch demo play limit:').pack(padx=5,pady=5,side='left')
        self.patch_demo_true=ttk.Radiobutton(t3_frm4,text='Yes',variable=self.patch_demo,value=True)
        self.patch_demo_false=ttk.Radiobutton(t3_frm4,text='No',variable=self.patch_demo,value=False)
        self.patch_demo_true.pack(padx=5,pady=5,side='left')
        self.patch_demo_false.pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t3_frm5,text='Patch DLC:').pack(padx=5,pady=5,side='left')
        self.patch_dlc_true=ttk.Radiobutton(t3_frm5,text='Yes',variable=self.patch_dlc,value=True)
        self.patch_dlc_false=ttk.Radiobutton(t3_frm5,text='No',variable=self.patch_dlc,value=False)
        self.patch_dlc_true.pack(padx=5,pady=5,side='left')
        self.patch_dlc_false.pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t3_frm6,text='Tickets only mode:').pack(padx=5,pady=5,side='left')
        self.tickets_only_true=ttk.Radiobutton(t3_frm6,text='On',variable=self.tickets_only,value=True)
        self.tickets_only_false=ttk.Radiobutton(t3_frm6,text='Off',variable=self.tickets_only,value=False)
        self.tickets_only_true.pack(padx=5,pady=5,side='left')
        self.tickets_only_false.pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t3_frm7,text='Simulation mode:').pack(padx=5,pady=5,side='left')
        self.simulate_mode_true=ttk.Radiobutton(t3_frm7,text='On',variable=self.simulate_mode,value=True)
        self.simulate_mode_false=ttk.Radiobutton(t3_frm7,text='Off',variable=self.simulate_mode,value=False)
        self.simulate_mode_true.pack(padx=5,pady=5,side='left')
        self.simulate_mode_false.pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t3_frm8,text='Download ALL titles on NUS except system\ntitles. Choose the regions you would like:').pack(padx=5,pady=5,side='left')
        self.region_box_usa=ttk.Checkbutton(t3_frm8,text='USA',variable=self.region_usa).pack(padx=5,pady=5,side='left')
        self.region_box_eur=ttk.Checkbutton(t3_frm8,text='EUR',variable=self.region_eur).pack(padx=5,pady=5,side='left')
        self.region_box_jpn=ttk.Checkbutton(t3_frm8,text='JPN',variable=self.region_jpn).pack(padx=5,pady=5,side='left')
        btn=ttk.Button(t3_frm8,text='Go',width=4,command=lambda:self.download_clicked(4)).pack(pady=20,side='left')
                
        t3_frm1.grid(row=1,column=1,sticky='w')
        t3_frm2.grid(row=2,column=1,sticky='w')
        t3_frm3.grid(row=3,column=1,sticky='w')
        t3_frm4.grid(row=4,column=1,sticky='w')
        t3_frm5.grid(row=5,column=1,sticky='w')
        t3_frm6.grid(row=6,column=1,sticky='w')
        t3_frm7.grid(row=7,column=1,sticky='w')
        t3_frm8.grid(row=8,column=1,padx=10,pady=70,sticky='w')

        # Tab 4
        t4_frm0=ttk.Frame(tab4)
        t4_frm1=ttk.Frame(tab4)
        t4_frm2=ttk.Frame(tab4)
        t4_frm3=ttk.Frame(tab4)
        t4_frm4=ttk.Frame(tab4)
        t4_frm5=ttk.Frame(tab4)
        t4_frm6=ttk.Frame(tab4)
        t4_frm7=ttk.Frame(tab4)
        t4_frm8=ttk.Frame(tab4)
        t4_frm9=ttk.Frame(tab4)
        t4_frm10=ttk.Frame(tab4)
        t4_frm11=ttk.Frame(tab4)

        lbl=ttk.Label(t4_frm0,text='Version Information:\n\nSince the FunKii-UI GUI and FunKiiU are two seperate applications developed by different authors,\nswitching versions can break compatibility and shouldn\'t be done if you don\'t know what you are\ndoing. I will try to implement a compatibility list in a future release').pack(padx=5,pady=1,side='left')
        lbl=ttk.Label(t4_frm1,text='GUI application:',font="Helvetica 13 bold").pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t4_frm2,text='Running version:\nTargeted for:').pack(padx=5,pady=1,side='left')
        lbl=ttk.Label(t4_frm2,text=__VERSION__+'\n'+targetversion).pack(padx=5,pady=1,side='left')
        lbl=ttk.Label(t4_frm3,text='Latest release:').pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t4_frm3,text=self.versions['gui_new']).pack(padx=5,pady=1,side='left')
        lbl=ttk.Label(t4_frm4,text='Update to latest release:').pack(padx=5,pady=1,side='left')
        btn=ttk.Button(t4_frm4,text='Update',command=lambda:self.update_application('gui',self.versions['gui_new'])).pack(padx=5,pady=1,side='left')
        lbl=ttk.Label(t4_frm5,text='Switch to different version:').pack(padx=5,pady=1,side='left')
        self.gui_switchv_box=ttk.Combobox(t4_frm5,width=7,values=[x for x in self.versions['gui_all']],state='readonly')
        self.gui_switchv_box.pack(padx=5,pady=1,side='left')
        btn=ttk.Button(t4_frm5,text='Switch',command=lambda:self.update_application('gui',self.gui_switchv_box.get())).pack(padx=5,pady=1,side='left')        
        lbl=ttk.Label(t4_frm6,text='').pack(pady=15,side='left')
        lbl=ttk.Label(t4_frm7,text='FunKiiU core application:',font="Helvetica 13 bold").pack(padx=5,pady=5,side='left')
        lbl=ttk.Label(t4_frm8,text='running version:').pack(padx=5,pady=1,side='left')
        lbl=ttk.Label(t4_frm8,text=fnku.__VERSION__).pack(padx=5,pady=1,side='left')
        lbl=ttk.Label(t4_frm9,text='latest release:').pack(padx=5,pady=1,side='left')
        lbl=ttk.Label(t4_frm9,text=self.versions['fnku_new']).pack(padx=5,pady=1,side='left')
        lbl=ttk.Label(t4_frm10,text='Update to latest release:').pack(padx=5,pady=1,side='left')
        btn=ttk.Button(t4_frm10,text='Update',command=lambda:self.update_application('fnku',self.versions['fnku_new'])).pack(padx=5,pady=1,side='left')
        lbl=ttk.Label(t4_frm11,text='Switch to different version:').pack(padx=5,pady=1,side='left')
        self.fnku_switchv_box=ttk.Combobox(t4_frm11,width=7,values=[x for x in self.versions['fnku_all']],state='readonly')
        self.fnku_switchv_box.pack(padx=5,pady=1,side='left')
        btn=ttk.Button(t4_frm11,text='Switch',command=lambda:self.update_application('fnku',self.fnku_switchv_box.get())).pack(padx=5,pady=1,side='left')

        t4_frm0.grid(row=0,column=1,padx=5,pady=5,sticky='w')
        t4_frm1.grid(row=1,column=1,padx=5,sticky='w')
        t4_frm2.grid(row=2,column=1,padx=25,sticky='w')
        t4_frm3.grid(row=3,column=1,padx=25,sticky='w')
        t4_frm4.grid(row=4,column=1,padx=25,sticky='w')
        t4_frm5.grid(row=5,column=1,padx=25,sticky='w')
        t4_frm6.grid(row=6,column=1,padx=5,sticky='w')
        t4_frm7.grid(row=7,column=1,padx=5,sticky='w')
        t4_frm8.grid(row=8,column=1,padx=25,sticky='w')
        t4_frm9.grid(row=9,column=1,padx=25,sticky='w')
        t4_frm10.grid(row=10,column=1,padx=25,sticky='w')
        t4_frm11.grid(row=11,column=1,padx=25,sticky='w')

    def update_keysite_widgets(self):
        txt='Correct keysite is already loaded'
        self.enterkeysite_lbl.configure(text=txt,background='black',foreground='green',font="Helvetica 13 bold")
        self.http_lbl.pack_forget()
        self.keysite_box.pack_forget()
        self.submitkeysite_btn.pack_forget()
        
    def check_config_keysite(self):
        try:
            with open('config.json') as cfg:
                config=json.load(cfg)                
                site=config['keysite']
                if fnku.hashlib.md5(site.encode('utf-8')).hexdigest() == fnku.KEYSITE_MD5:
                    self.update_keysite_widgets()
                    
        except IOError:
            pass
        
    def notify_of_update(self,update=True):
        #print('UPDATES ARE AVAILABLE')
        txt='Updates are available in the updates tab'
        fg='red'
        if not update:
            txt='No updates are currently available'
            fg='green'
        self.updatelabel.configure(text=txt,background='black',foreground=fg,font="Helvetica 13 bold")
        
    def update_application(self,app,zip_file):
        if app == 'fnku':
            self.download_zip(self.versions['fnku_url'].split('releases')[0]+'archive'+'/v'+zip_file+'.zip')
        else:
            self.download_zip(self.versions['gui_url'].split('releases')[0]+'archive'+'/v'+zip_file+'.zip')
            
        if self.unpack_zip('update.zip'):
            print('Update completed succesfully! Restart application\nfor changes to take effect.')

    def unpack_zip(self,zip_name):
        try:
            print('unzipping update')
            cwd=os.getcwd()
            dest=cwd+dir_slash+zip_name
            zfile=zipfile.ZipFile(dest,'r')
            for i in zfile.namelist():
                data=zfile.read(i,None)
                x=i.split("/")[1]
                if x!='':
                    with open(x,'wb') as p_file:
                        p_file.write(data)                      
            zfile.close()           
            return True
        
        except Exception as e:
            print('Error:',e)
            return False
        
    def download_zip(self,url):
        try:
            z = urlopen(url)
            print('Downloading ', url)      
            with open('update.zip', "wb") as f:
                f.write(z.read())
            print('\nDone.')
            
        except HTTPError as e:
            print("Error:", e.code, url)
        except URLError as e:
            print ("Error:", e.reason, url)
                   
    def populate_selection_box(self,download_data=True):
        if download_data:
            keysite = fnku.get_keysite()
            print(u'Downloading/updating data from {0}'.format(keysite))

            if not fnku.download_file('https://{0}/json'.format(keysite), 'titlekeys.json', 3):
                print('ERROR: Could not download data file...\n')
            else:
                print('DONE....Downloaded titlekeys.json succesfully')
        try:
            self.clear_id_key_boxes()
            self.selection_list=[]    
            self.load_title_data()
            if self.filter_usa.get():
                if self.filter_game.get():
                    for i in self.usa_selections['game']:
                        self.selection_list.append(i)
                if self.filter_dlc.get():
                    for i in self.usa_selections['dlc']:
                        self.selection_list.append(i)
                if self.filter_update.get():
                    for i in self.usa_selections['update']:
                        self.selection_list.append(i)
                    
            if self.filter_eur.get():
                if self.filter_game.get():
                    for i in self.eur_selections['game']:
                        self.selection_list.append(i)
                if self.filter_dlc.get():
                    for i in self.eur_selections['dlc']:
                        self.selection_list.append(i)
                if self.filter_update.get():
                    for i in self.eur_selections['update']:
                        self.selection_list.append(i)
                        
            if self.filter_jpn.get():
                if self.filter_game.get():
                    for i in self.jpn_selections['game']:
                        self.selection_list.append(i)
                if self.filter_dlc.get():
                    for i in self.jpn_selections['dlc']:
                        self.selection_list.append(i)
                if self.filter_update.get():
                    for i in self.jpn_selections['update']:
                        self.selection_list.append(i)
                        
            self.selection_list.sort()
            self.selection_box.set('')
            self.selection_box.configure(values=(self.selection_list))
            self.selection_box.set_completion_list(self.selection_list)
            print('Succesfully populated the selection box..')
        except Exception as e:
            print('Something happened while trying to populate the selection box...')
            print('ERROR:' ,e)

    def clear_id_key_boxes(self,*args):
        self.id_box.delete('0',tk.END)
        self.key_box.delete('0',tk.END)
        
    def selection_box_changed(self,*args):
        self.clear_id_key_boxes()
        user_selected_raw=self.selection_box.get()
        x=user_selected_raw.split('--')
        sel_name=x[0].strip()
        
        sel_region=x[1].split('-')[0].strip()
        sel_type=x[1].split('-')[1].strip()
        
        for i in self.title_data:
            if i[0] == sel_name and i[1] == sel_region and i[4] == sel_type:
                titleid=i[2]
                key=i[3]
                
                self.id_box.insert('end',titleid)
                if key != 'None': self.key_box.insert('end',key)
                break
    
    def load_title_data(self):       
        self.title_data=[]
        try:
            with open('titlekeys.json') as td:
                title_data=json.load(td)                
            self.errors=0
            print('Now parsing titlekeys.json')
            for i in title_data:
                try:
                    if i['name']:
                        name=str(i['name']).lower().capitalize().strip()
                        titleid=str(i['titleID'])
                        titlekey=str(i['titleKey'])
                        region=str(i['region'])
                        if titleid[4:8] == '0000':
                            content_type='GAME'
                        elif titleid[4:8] == '000c':
                            content_type='DLC'
                        elif titleid[4:8] == '000e':
                            content_type='UPDATE'
                        entry=(name,region,titleid,titlekey,content_type)
                        entry2=(name+'  --'+region+'  -'+content_type)
                        if not entry in self.title_data:
                            self.title_data.append(entry)
                            if region == 'USA':
                                if content_type == 'GAME':
                                    if not entry2 in self.usa_selections['game']:
                                        self.usa_selections['game'].append(entry2)
                                elif content_type == 'DLC':
                                    if not entry2 in self.usa_selections['dlc']:
                                        self.usa_selections['dlc'].append(entry2)
                                elif content_type == 'UPDATE':
                                    if not entry2 in self.usa_selections['update']:
                                        self.usa_selections['update'].append(entry2)
                            elif region == 'EUR':
                                if content_type == 'GAME':
                                    if not entry2 in self.eur_selections['game']:
                                        self.eur_selections['game'].append(entry2)
                                elif content_type == 'DLC':
                                    if not entry2 in self.eur_selections['dlc']:
                                        self.eur_selections['dlc'].append(entry2)
                                elif content_type == 'UPDATE':
                                    if not entry2 in self.eur_selections['update']:
                                        self.eur_selections['update'].append(entry2)
                            elif region == 'JPN':
                                if content_type == 'GAME':
                                    if not entry2 in self.jpn_selections['game']:
                                        self.jpn_selections['game'].append(entry2)
                                elif content_type == 'DLC':
                                    if not entry2 in self.jpn_selections['dlc']:
                                        self.jpn_selections['dlc'].append(entry2)
                                elif content_type == 'UPDATE':
                                    if not entry2 in self.jpn_selections['update']:
                                        self.jpn_selections['update'].append(entry2)
                                    
                #Some entries in titlekeys.json are invalid,or just not encoding right, or I'm doing something wrong.
                #Passing errors silently for now.
                except Exception as e:
                    pass
                    if DEBUG:
                        print('ERROR LOADING ',e)
                        self.errors+=1
        except IOError:
            print('No titlekeys.json file was found. The selection box will be empty')
        if DEBUG: print(str(self.errors)+' Titles did not load correctly.')
         
    def sanity_check_input(self,val,chktype):
        try:
            if chktype == 'title':
                if len(val) == 16:
                    val=int(val,16)
                    return True
            elif chktype =='key':
                if len(val) == 32:
                    val=int(val,16)
                    return True
            else:
                return False
        except ValueError:
            return False
        
    def add_to_list(self):
        titleid = self.id_box.get().strip()
        name = self.selection_box.get().strip()
        if name == '':
            name = titleid
        for i in self.title_data:
            if titleid == i[2]:
                name = i[0]
                region = i[1]
                content_type = i[4]
                name = name+'  --'+region+'  '+content_type
                break
        if self.sanity_check_input(titleid,'title'):
            pass
        else:
            print('Bad Title ID. Must be a 16 digit hexadecimal.')
            return
        key=self.key_box.get().strip()
        if key == '':
            key=None
            
        else:
            if self.sanity_check_input(key,'key') or not key:
                pass
            else:
                print('Bad Key. Must be a 16 digit hexadecimal.')
                return
        if key: name=name+' **'
        entry=(name,titleid,key)
        if not entry in self.download_list: self.download_list.append(entry)
        self.populate_dl_listbox()

    def remove_from_list(self):
        try:
            index=self.dl_listbox.curselection()
            item=self.dl_listbox.get('active')
            for i in self.download_list:
                if i[0] == item:
                    self.download_list.remove(i)
            self.populate_dl_listbox()
        except IndexError as e:
            print('Download list is already empty')
            print(e)

    def clear_list(self):
        self.download_list=[]
        self.populate_dl_listbox()
        
    def populate_dl_listbox(self):
        self.dl_listbox.delete('0',tk.END)
        for i in self.download_list:
            self.dl_listbox.insert('end',i[0])

    def submit_key_site(self):
        site=self.keysite_box.get().strip()
        if fnku.hashlib.md5(site.encode('utf-8')).hexdigest() == fnku.KEYSITE_MD5:
            print('Correct key site, now saving...')
            config=fnku.load_config()
            config['keysite'] = site
            fnku.save_config(config)
            print('done saving, you are good to go!')
            self.update_keysite_widgets()
            self.nb.select(self.tab2)
        else:
            print('Wrong key site provided. Try again')

    def get_output_directory(self):
        out_dir=filedialog.askdirectory()
        self.out_dir_box.delete('0',tk.END)
        self.out_dir_box.insert('end',out_dir)

    def load_program_revisions(self):
        print('Checking for program updates, this might take a few seconds.......\n')
        url1=self.versions['fnku_url']
        url2=self.versions['gui_url']    
        response = urlopen(url1)
        rslts=response.read()
        rslts=str(rslts)
        x=''
        for i in rslts:
            x=x+i
        parser = VersionParser()
        parser.feed(x)
        response = urlopen(url2)
        rslts=response.read()
        rslts=str(rslts)
        x=''
        for i in rslts:
            x=x+i
        parser = VersionParser()
        parser.feed(x)

        fnku_data_set = parser.fnku_data_set
        gui_data_set = parser.gui_data_set
        
        fnku_all=[]
        fnku_newest=''
        gui_all=[]
        gui_newest=''
        
        for i in fnku_data_set:
            ver=LooseVersion(i.split('/')[4][1:-4])
            fnku_all.append(str(ver))
        fnku_newest=max(fnku_all)
        
        for i in gui_data_set:
            ver=LooseVersion(i.split('/')[4][1:-4])
            if ver > LooseVersion('2.0.5'):
                gui_all.append(ver)
                
        gui_newest=max(gui_all)
        if gui_newest > current_gui or fnku_newest > current_fnku:
            self.notify_of_update()
        else:
            self.notify_of_update(update=False)
            

        self.versions['fnku_all']=fnku_all
        self.versions['fnku_new']=fnku_newest
        self.versions['gui_all']=[str(i) for i in gui_all]
        self.versions['gui_new']=str(gui_newest)
        
    def download_clicked(self,dl_method):
        title_list=[]
        key_list=[]
        output_dir=self.output_dir.get().strip()
        if len(output_dir)==0:
            output_dir=None
        retry_count=self.retry_count.get()
        patch_demo=self.patch_demo.get()
        patch_dlc=self.patch_dlc.get()
        tickets_only=self.tickets_only.get()
        simulate=self.simulate_mode.get()
        for i in self.download_list:
            if not i[1] in title_list:
                title_list.append(i[1])
                if i[2]:
                    if not i[2] in key_list:
                        key_list.append(i[2])
        if dl_method == 1:
            fnku.main(titles=title_list,onlinetickets=True,output_dir=output_dir,retry_count=retry_count,
                      patch_demo=patch_demo,patch_dlc=patch_dlc,tickets_only=tickets_only,simulate=simulate)
        elif dl_method == 2:
            fnku.main(titles=title_list,onlinekeys=True,output_dir=output_dir,retry_count=retry_count,
                      patch_demo=patch_demo,patch_dlc=patch_dlc,tickets_only=tickets_only,simulate=simulate)
        elif dl_method == 3:
            if len(title_list) == len(key_list):
                fnku.main(titles=title_list,keys=key_list,output_dir=output_dir,retry_count=retry_count,
                          patch_demo=patch_demo,patch_dlc=patch_dlc,tickets_only=tickets_only,simulate=simulate)
            else:
                print('Number of Keys provided does not match the number of Titles provided')
        elif dl_method == 4:
            regions=[]
            if self.region_usa.get():
                regions.append('USA')
            if self.region_eur.get():
                regions.append('EUR')
            if self.region_jpn.get():
                regions.append('JPN')
            if len(regions)>0:
                fnku.main(download_regions=regions,output_dir=output_dir,retry_count=retry_count,
                          patch_demo=patch_demo,patch_dlc=patch_dlc,tickets_only=tickets_only,simulate=simulate)
            else:
                print('No regions selected. Try again.')
            
                
    
        
if __name__ == '__main__':
    root=RootWindow()
    root.title('FunKii-UI')
    root.resizable(width=False,height=False)
    root.mainloop()
