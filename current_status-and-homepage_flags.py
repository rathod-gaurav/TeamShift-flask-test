while(True):
    config = pd.read_csv('config/config.csv', sep=',')

    #update homepage flags
    homepage_flags = pd.read_csv('files/homepage_flags.csv', sep=',')

    ts = time.localtime()
    readable_ts_2 = time.strftime("%Y-%m-%d %H:%M:%S", ts)

    for i in range(len(config.index)):
        if(readable_ts_2 == config.loc[i][1]):
            message = f"Current Growth Phase : {config.loc[i][0]}"
            if(homepage_flags.empty):
                homepage_flags = homepage_flags.append({'Timestamp' : config.loc[i][1], 'Message' : message})
                homepage_flags.to_csv("files/homepage_flags.csv", index=False)
            elif(message in homepage_flags['Message']):
                break
            else:
                homepage_flags = homepage_flags.append({'Timestamp' : config.loc[i][1], 'Message' : message})
                homepage_flags.to_csv("files/homepage_flags.csv", index=False)
        elif(readable_ts_2 == config.loc[i][2]):
            message = f"Change in Plant's Growth Phase : {config.loc[i][0]} => {config.loc[i+1][0]}"
            if(homepage_flags.empty):
                homepage_flags = homepage_flags.append({'Timestamp' : config.loc[i][2], 'Message' : message})
                homepage_flags.to_csv("files/homepage_flags.csv", index=False)
            if(message in homepage_flags['Message']):
                break
            else:
                homepage_flags = homepage_flags.append({'Timestamp' : config.loc[i][2], 'Message' : message})
                homepage_flags.to_csv("files/homepage_flags.csv", index=False)
    

    #update current status    
    current_status = pd.read_csv('files/current_status.csv', sep=',')

    for i in range(len(config.index)):
        if(readable_ts_2 == config.loc[i][1]):
            if(current_status.empty):
                current_status = current_status.append(config.loc[i])
                current_status.to_csv("files/current_status.csv", index=False)
            elif(config.loc[i][0] in current_status.iloc[0][0]):
                break
            else:
                current_status = current_status.append(config.loc[i])
                current_status.to_csv("files/current_status.csv", index=False)
