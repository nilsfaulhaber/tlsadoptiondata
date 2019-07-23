import pandas as pd
import datetime
import os
import numpy as np

PERFORMANCE_DATA_DIRECTORY =  "/data/tlsadoptiondata/Performance/"
OUTPUT_FOLDER = "/data/monitoring-tls13-adoption/tlsadoptiondata/Performance/v6/"
def get_file_names_sorted():
    name_list =  [os.fsdecode(file) for file in os.listdir(OUTPUT_FOLDER)]
    name_list_clean = list(filter(lambda x: 'performance_output' in x, name_list))
    return sorted(name_list_clean, key= lambda name: datetime.datetime.strptime(name[18:28], '%Y-%m-%d'))



def write_data_for_url(url, dataTLS12df, dataTLS13df, urls_to_values_12, urls_to_values_13, urls_to_conn_diff):
        connection_est_time_13 = dataTLS13df[dataTLS13df.Url == url].loc[0:, "ConnectionEstablishmentTime"]
        if (len(connection_est_time_13.index) != 0):
            if url in urls_to_values_13.keys():
                val = urls_to_values_13[url]
                val.append(connection_est_time_13.values[0])
                urls_to_values_13[url] = val
            else:
                urls_to_values_13[url] = [connection_est_time_13.values[0]]

        connection_est_time_12 = dataTLS12df[dataTLS12df.Url == url].loc[0:, "ConnectionEstablishmentTime"]
        if (len(connection_est_time_12.index) != 0):
            if url in urls_to_values_12.keys():
                val = urls_to_values_12[url]
                val.append(connection_est_time_12.values[0])
                urls_to_values_12[url] = val
            else:
                urls_to_values_12[url] = [connection_est_time_12.values[0]]

        if (len(connection_est_time_12.index) != 0 and len(connection_est_time_13.index) != 0):
            diff = connection_est_time_12.values[0] - connection_est_time_13.values[0]
            if url in urls_to_conn_diff.keys():
                val = urls_to_conn_diff[url]
                val.append(diff)
                urls_to_conn_diff[url] = val
            else:
                urls_to_conn_diff[url] = [diff]
        return (urls_to_values_12, urls_to_values_13, urls_to_conn_diff)


def get_urls_to_values(mode):
    if mode == "TLS1.2":
        with open(OUTPUT_FOLDER + "tls12_performance_per_url_v6.txt", 'r') as f:
            content = f.readlines()
            urls_to_values = {}
            for line in content:
                (url, performance12_data_raw) = line.split(";")
                performance12_data_dirty = performance12_data_raw.split(',')
                performance12_data = []
                for value in performance12_data_dirty:
                    try:
                        performance12_data.append(float(value))
                    except Exception:
                        continue
                urls_to_values[url] = performance12_data
        return urls_to_values
    elif mode == "TLS1.3":
        with open(OUTPUT_FOLDER + "tls13_performance_per_url_v6.txt", 'r') as f:
            content = f.readlines()
            urls_to_values = {}
            for line in content:
                (url, performance13_data_raw) = line.split(";")
                performance13_data_dirty = performance13_data_raw.split(',')
                performance13_data = []
                for value in performance13_data_dirty:
                    try:
                        performance13_data.append(float(value))
                    except Exception:
                        continue
                urls_to_values[url] = performance13_data
        return urls_to_values
    else:
        with open(OUTPUT_FOLDER + "conn_diff_per_url_v6.txt", 'r') as f:
            content = f.readlines()
            urls_to_values = {}
            for line in content:
                (url, conn_diff_data_raw) = line.split(";")
                conn_diff_data_dirty = conn_diff_data_raw.split(',')
                conn_diff_data = []
                for value in conn_diff_data_dirty:
                    try:
                        conn_diff_data.append(float(value))
                    except Exception:
                        continue
                urls_to_values[url] = conn_diff_data
        return urls_to_values


def write_dict_to_file(dict, file):
    with open(file, "w") as f:
        for url in dict.keys():
            f.write(url + ";")
            for value in dict[url]:
                f.write(str(value) + ",")
            f.write("\n")

def write_data_to_files():

    files = get_file_names_sorted()
    dates = []
    with open(OUTPUT_FOLDER + 'dates_v6.txt', 'r') as f:
        content = f.readlines()
        dates = [x.strip() for x in content]
    for filename in files:
        connection_differences = []
        file_date = filename[18:28]
        if file_date in dates:
            continue
        df_current = pd.read_csv(OUTPUT_FOLDER + filename, ";")
        print("Processing " + filename)
        performance13_data = df_current[df_current.Protocol == "TCP/TLS1.3"].loc[0:,
                             "ConnectionEstablishmentTime"].dropna().values.tolist()

        performance12_data = df_current[df_current.Protocol == "TCP/TLS1.2"].loc[0:,
                             "ConnectionEstablishmentTime"].dropna().values.tolist()

        dataTLS13df = df_current[df_current.Protocol == "TCP/TLS1.3"].loc[0:,
                      ["Asn", "Holder", "Ip", "Url", "ConnectionEstablishmentTime"]]
        dataTLS12df = df_current[df_current.Protocol == "TCP/TLS1.2"].loc[0:,
                      ["Asn", "Holder", "Ip", "Url", "ConnectionEstablishmentTime"]]

        urls_to_values_12 = get_urls_to_values("TLS1.2")
        urls_to_values_13 = get_urls_to_values("TLS1.3")
        urls_to_conn_diff = get_urls_to_values("ConnDiff")

        for index, row in dataTLS12df.iterrows():
            url = dataTLS13df['Url'] == row['Url']
            t = dataTLS13df[url]
            t = t.reset_index(drop=True)
            if not (t.empty):
                diff = row['ConnectionEstablishmentTime'] - t.at[0, 'ConnectionEstablishmentTime']
                connection_differences.append(
                    [t.at[0, "Asn"], t.at[0, "Holder"], t.at[0, 'Url'], t.at[0, 'Ip'], (diff)])
                dfTls13Tls12 = pd.DataFrame(connection_differences,
                                            columns=['Asn', "Holder" 'URL', 'IP', 'PORT', 'ConnDiff'])
                (urls_to_values_12, urls_to_values_13, urls_to_conn_diff) = write_data_for_url(t.at[0, "Url"],
                                                                                               dataTLS12df, dataTLS13df,
                                                                                               urls_to_values_12,
                                                                                               urls_to_values_13,
                                                                                               urls_to_conn_diff)
                write_dict_to_file(urls_to_values_12, OUTPUT_FOLDER + "tls12_performance_per_url_v6.txt")
                write_dict_to_file(urls_to_values_13, OUTPUT_FOLDER + "tls13_performance_per_url_v6.txt")
                write_dict_to_file(urls_to_conn_diff, OUTPUT_FOLDER + "conn_diff_per_url_v6.txt")
        vals_sorted = np.sort(dfTls13Tls12['ConnDiff'].dropna())
        with open(OUTPUT_FOLDER + 'dates_v6.txt', 'a') as f:
            f.write(file_date + "\n")
        with open(OUTPUT_FOLDER + 'tls13_performance_data_v6.txt', 'a') as f:
            f.write(file_date + ";")
            for value in performance13_data:
                f.write(str(value) + ",")
            f.write("\n")
        with open(OUTPUT_FOLDER + 'tls12_performance_data_v6.txt', 'a') as f:
            f.write(file_date + ";")
            for value in performance12_data:
                f.write(str(value) + ",")
            f.write("\n")
        with open(OUTPUT_FOLDER + 'connection_differences_v6.txt', 'a') as f:
            f.write(file_date + ";")
            for value in vals_sorted:
                f.write(str(value) + ",")
            f.write("\n")


write_data_to_files()
