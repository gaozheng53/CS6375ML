import sys
import json
import re
import logging
import numpy as np
import pandas as pd

logging.basicConfig()
logger = logging.getLogger('tweet')
logger.setLevel(logging.INFO)

# read tweet and convert them to a list including text and id
def parse_tweets_json(jsonpath):
    logger.info('Starting to read '+jsonpath)
    tweets = []
    readin = open(jsonpath)
    for line in readin:
        row=[]
        linein = json.loads(line)
        text = linein["text"]
        row.append(text)
        idin = linein["id"]
        row.append(idin)
        tweets.append(row)
    logger.info('Finishing to read '+jsonpath)

    logger.info('Starting to parse '+jsonpath)
    for i in range(len(tweets)):
        tweets[i][0]=re.sub('[@#]\w*','',tweets[i][0])
        tweets[i][0]=re.sub(':','',tweets[i][0])
        tweets[i][0]=re.sub('RT','',tweets[i][0])
        tweets[i][0]=re.sub('\w*//?\w*','',tweets[i][0])
        tweets[i][0]=tweets[i][0].split(" ")
    logger.info('Finishing to parse '+jsonpath)
    return tweets

# input the initial centroids and their contents
def init_centroid(initialSeedsFile, tweets):
    logger.info('Starting to initializing centroid')
    center=pd.read_csv(initialSeedsFile,header=None)
    center=center[0]
    centroid=[]
    for point in center:
        row=[]
        row.append(point)
        for data in tweets:
            if point == data[1]:
                row.append(data[0])
        centroid.append(row)
    logger.info('Finishing to initializing centroid')
    return centroid

# calculate the Jaccard distance
def jaccard_distance(list1, list2):
    U=len(set(list1).union(set(list2)))
    I=len(set(list1).intersection(set(list2)))
    dist=(U-I)/U
    return dist


def k_mean(data, centroid, kclusters=25):
    logger.info('Starting clustering')
    data=np.array(data)
    # add one column to store assigned clusters
    col1=np.zeros((data.shape[0],1))
    data=np.append(data,col1,axis=1)
    col2=np.zeros((data.shape[0],1))
    data=np.append(data,col2,axis=1)

    for n in range(20):
        for i in range(data.shape[0]):
            min=sys.maxsize
            for j in range(kclusters):
                dist=jaccard_distance(data[i][0],centroid[j][1])
                if min>dist:
                    min=dist
                    data[i][2]=centroid[j][0]
                    data[i][3]=min

        for i in range(kclusters):
            subdata=[]
            for j in range(data.shape[0]):
                row=[]
                if data[j][2]==centroid[i][0]:
                    row.append(data[j][0])
                    row.append(data[j][1])
                    subdata.append(row)
            min=sys.maxsize
            for j in range(len(subdata)):
                total=0
                for k in range(len(subdata)):
                    dist=jaccard_distance(subdata[j][0], subdata[k][0])
                    total +=dist
                if total<min:
                    min=total
                    centroid[i][0]=subdata[j][1]
    logger.info('Finishing clustering')
    return data,centroid


def main(argv):

    numberOfClusters, initialSeedsFile, TweetsDataFile, outputFile = argv[1:]
    numberOfClusters = int(numberOfClusters)

    tweets = parse_tweets_json(TweetsDataFile)
    centroid = init_centroid(initialSeedsFile, tweets)
    data,centroid=k_mean(tweets,centroid,numberOfClusters)
    data=pd.DataFrame(data).iloc[:,1:]
    data.columns=['id','cluster_id','distance']

    # format output
    result = []
    for cluster_id in range(len(centroid)):
        centroid_row = centroid[cluster_id]
        centroid_id = centroid_row[0]
        logger.info("Processing cluster "+str(cluster_id+1)+" with centroid "+str(centroid_id))

        cluster_elemets = data[data['cluster_id'] == centroid_id]
        cluster_size = cluster_elemets.shape[0]

        avg_dist = 0
        tweets_in_cluster = []
        if cluster_size>0:
            for index, row in cluster_elemets.iterrows():
                avg_dist += row['distance']
                tweets_in_cluster.append(row['id'])

            avg_dist = avg_dist/cluster_size
            result.append([cluster_id+1,centroid_id,cluster_size,avg_dist,str(tweets_in_cluster)])

    result=pd.DataFrame(result)
    result.columns = ['cluster_id','centroid_id','cluster_size','average_distance','list_of_tweet_id']
    # print(result)
    logger.info('Starting to write output file '+outputFile)
    result.to_csv(outputFile,index=False)
    logger.info('Finishing to write output file '+outputFile)

if __name__ == '__main__':
    # tweets-k-means <numberOfClusters> <initialSeedsFile> <TweetsDataFile> <outputFile>
    # python3 tweets-k-means.py 25 initialSeeds.txt Tweets.json k-means-result.csv
    main(sys.argv)
