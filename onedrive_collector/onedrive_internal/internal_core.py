from onedrive_collector.onedrive_internal.collector import *
from onedrive_collector.onedrive_internal.personal_vault import *
import module.Cloud_Display as cd

class OneDrive_Internal:
    def __init__(self):
        self.__flag = None
        self.__mode = None
        pass

    def run(self, credential):
        cd.start_internal()
        self.__flag = int(input("Do you want open \'PERSONAL VAULT\'? (1:Yes, 0:No) >>"))

        PRINTI("Start OneDrive Module - <Internal Mode>")
        if self.__flag == 0:
            a, a_result = self.__call_auth(credential)
            if a_result == CA_ERROR:
                PRINTI("OneDrive Authentication ERROR")
                return CA_ERROR

            e, e_result = self.__call_explorer(a)
            if e_result == CA_ERROR:
                PRINTI("OneDrive Exploration ERROR")
                return CA_ERROR

            c_result = self.__call_collector(e, a)
            if c_result == CA_ERROR:
                PRINTI("OneDrive Collector ERROR")
                return CA_ERROR
        else:
            p, p_result = self.__call_pv(credential)
            if p_result == CA_ERROR:
                PRINTI("OneDrive Authentication ERROR (Personal Vault Version)")
                return CA_ERROR

        PRINTI("End OneDrive Module - <Internal Mode>")

    @staticmethod
    def __call_pv(credential):
        PRINTI("OneDrive (Personal Vault Version) .... Start")
        pv = Personal_Vault(credential=credential)
        p_result = pv.run()
        PRINTI("OneDrive (Personal Vault Version) .... End")
        return pv, p_result

    @staticmethod
    def __call_auth(credential):
        PRINTI("OneDrive Authentication .... Start")
        auth_data = Authentication(credential=credential)
        a_result = auth_data.run()
        PRINTI("OneDrive Authentication .... End")
        return auth_data, a_result

    @staticmethod
    def __call_explorer(auth_data):
        PRINTI("OneDrive Exploration .... Start")
        e = Exploration(auth_data)
        e_result = e.run()
        PRINTI("OneDrive Exploration .... End")
        return e, e_result

    @staticmethod
    def __call_collector(onedrive_data, auth_data):
        c = Collector(onedrive_data, auth_data)
        file_len = c.get_num_of_file_list()
        c.set_file_list()
        while True:
            try:
                menu = cd.select_menu()
            except:
                PRINTE("Please Input Correct Number")
                continue
            if menu == 0:  # exit
                break
            elif menu == 1:  # all of file
                try:
                    show_menu = cd.select_show_menu()
                except:
                    PRINTE("Please Input Correct Number")
                    continue
                if show_menu == 0:
                    continue
                elif show_menu == 1:
                    c.show_file_list()
                elif show_menu == 2:
                    c.show_my_files_list()
                elif show_menu == 3:
                    c.show_recent_list()
                elif show_menu == 4:
                    c.show_shared_list()
                elif show_menu == 5:
                    c.show_recycle_list()
            elif menu == 2:  # select file
                c.show_file_list()
                file_len = c.get_num_of_file_list()
                while True:
                    try:
                        download_number = int(input("Put file numbers (exit:0): "))
                        if download_number == 0:
                            break

                        if download_number < 0:
                            print("\n Please Input correct number.")
                            continue
                        elif download_number > file_len:
                            print("Please Input correct number.")
                            continue
                        c.download_file(download_number)
                    except:
                        PRINTE("Please Input Correct Number")
            elif menu == 3:  # search
                try:
                    sm = cd.search_menu()
                except:
                    PRINTE("Please Input Correct Number")
                    continue
                s_input = CInput()
                if sm == 0:
                    continue
                elif sm == 1:
                    q = input("What do you want to search for? >> ")
                    c.search_file(q)
                elif sm == 2:
                    search_period = s_input.set_m_period()
                    if search_period[0] and search_period[1]:
                        if search_period[0] != '1970-01-01':
                            re_start_time = datetime.datetime.strptime(search_period[0],
                                                                       "%Y-%m-%d") - datetime.timedelta(days=1)
                            re_start_time = re_start_time.strftime("%Y-%m-%d")
                        else:
                            re_start_time = search_period[0]
                        s_period = re_start_time
                        e_period = datetime.datetime.strptime(search_period[1],
                                                                   "%Y-%m-%d") - datetime.timedelta(days=1)
                        e_period = e_period.strftime("%Y-%m-%d")
                        c.search_file_by_date(s_period, e_period)
                elif sm == 3:
                    q = input("What username do yo want >> ")
                    c.search_file_by_name(q)
            else:
                print(" [!] Invalid Menu. Choose Again.")
                continue
        return CA_OK