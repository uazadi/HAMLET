import glob, os
import re

count = 0



count_gain = 0


final = open("/home/umberto/Documents/HMMTweetChecker/src/training_sets/Means.csv", 'w+')
final.write("HMM;c_corr_mean;c_corr_SA_mean;c_corr_OA_mean;w_corr_mean;w_corr_SA_mean;w_corr_OA_mean;"
            "Sh_c_corr_mean;Sh_c_corr_SA_mean;Sh_c_corr_OA_mean;Sh_w_corr_mean;Sh_w_corr_SA_mean;Sh_w_corr_OA_mean;"
            "Gain_c;Gain_w;Sh_Gain_c;Sh_Gain_w\n")
final.close()

err_count = 0

os.chdir("/home/umberto/Documents/HMMTweetChecker/src/training_sets")
for res_file in glob.glob("/home/umberto/Documents/HMMTweetChecker/src/training_sets/*/Results.txt"):
    with open(res_file, 'r') as results:
        print res_file
        cmeans = []
        cstd = []
        csame_accont = []
        cother_account = []

        mmeans = []
        mstd = []
        msame_accont = []
        mother_account = []

        cmeans_shared = []
        cstd_shared = []
        csame_accont_shared = []
        cother_account_shared = []

        mmeans_shared = []
        mstd_shared = []
        msame_accont_shared = []
        mother_account_shared = []

        gain_w = []
        gain_c = []
        gain_w_shared = []
        gain_c_shared = []

        for line in results:
            if(re.search("^MEAN:.*", line)):
                if count == 0:
                    cmeans.append(float(line.split(" ")[-1]))
                if count == 1:
                    mmeans.append(float(line.split(" ")[-1]))
                if count == 2:
                    cmeans_shared.append(float(line.split(" ")[-1]))
                if count == 3:
                    mmeans_shared.append(float(line.split(" ")[-1]))
            if (re.search("^STD:.*", line)):
                if count == 0:
                    cstd.append(float(line.split(" ")[-1]))
                if count == 1:
                    mstd.append(float(line.split(" ")[-1]))
                if count == 2:
                    cstd_shared.append(float(line.split(" ")[-1]))
                if count == 3:
                    mstd_shared.append(float(line.split(" ")[-1]))
            if("SAME ACCOUNTS MEAN:" in line):
                if count == 0:
                    csame_accont.append(float(line.split(" ")[-1]))
                if count == 1:
                    msame_accont.append(float(line.split(" ")[-1]))
                if count == 2:
                    csame_accont_shared.append(float(line.split(" ")[-1]))
                if count == 3:
                    msame_accont_shared.append(float(line.split(" ")[-1]))
            if ("OTHER ACCOUNTS MEAN:" in line):
                if count == 0:
                    cother_account.append(float(line.split(" ")[-1]))
                if count == 1:
                    mother_account.append(float(line.split(" ")[-1]))
                if count == 2:
                    cother_account_shared.append(float(line.split(" ")[-1]))
                if count == 3:
                    mother_account_shared.append(float(line.split(" ")[-1]))
                    count = -1
                count = count + 1
            if ("WORD MEAN:" in line):
                if count_gain == 0:
                    gain_w.append(float(line.split(" ")[-1]))
                else:
                    gain_w_shared.append(float(line.split(" ")[-1]))
            #if ("WORD STD:" in line):
            if ("CHARS MEAN:" in line):
                if count_gain == 0:
                    gain_c.append(float(line.split(" ")[-1]))
                else:
                    gain_c_shared.append(float(line.split(" ")[-1]))
                    count_gain = -1
                    count_gain = count_gain + 1
            #if ("CHARS STD:" in line):
        final = open("/home/umberto/Documents/HMMTweetChecker/src/training_sets/Means.csv", 'a+')

        tweet = range(1400, 7001, 1400)
        tweet_count = 0
        tweet_index = 0
        max = [0.5, 0.75, 0]
        err = [10, 30, 20]
        max_count = 0

        for i in range(1, 30, 2):
            csv = str(err[err_count]) + "_" + str(tweet[tweet_index]) + "_" + str(max[max_count%3]) + ";"

            csv += str(cmeans[i-1]) + ";"
            csv += str(csame_accont[i-1]) + ";"
            csv += str(cother_account[i - 1]) + ";"
            csv += str(mmeans[i - 1]) + ";"
            csv += str(msame_accont[i - 1]) + ";"
            csv += str(mother_account[i - 1]) + ";"

            csv += str(cmeans[i]) + ";"
            csv += str(csame_accont[i]) + ";"
            csv += str(cother_account[i]) + ";"
            csv += str(mmeans[i]) + ";"
            csv += str(msame_accont[i]) + ";"
            csv += str(mother_account[i]) + ";"

            csv += str(gain_c[i-1]) + ";"
            csv += str(gain_w[i-1]) + ";"

            csv += str(gain_c[i]) + ";"
            csv += str(gain_w[i]) + "\n"


            tweet_count += 1
            max_count += 1

            if tweet_count == 3:
                tweet_index += 1
                tweet_count = 0
            final.write(csv)
        final.close()
        err_count += 1


print cmeans
print cstd
print csame_accont
print cother_account
print "---------------------------------------------"
print mmeans
print mstd
print msame_accont
print mother_account
print "---------------------------------------------"
print cmeans_shared
print cstd_shared
print csame_accont_shared
print cother_account_shared
print "---------------------------------------------"
print mmeans_shared
print mstd_shared
print msame_accont_shared
print mother_account_shared
print "---------------------------------------------"
print gain_w
print gain_c
print gain_w_shared
print gain_c_shared



