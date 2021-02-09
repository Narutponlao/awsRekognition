import boto3
import pprint

def add_faces_to_collection(bucket,photo,collection_id):
    client = boto3.client(
    "rekognition",
    aws_access_key_id="AKIAI6QFCNIR42EGCCLA",
    aws_secret_access_key="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",
    region_name="us-west-2"
)
    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=photo,
                                MaxFaces=5,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + photo)
    print('Faces indexed:')
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])

def check_person(collection_id,photo):


    maxResults=2
    faces_count=0

    count=0;
    tokens=True
    client = boto3.client(
        "rekognition",
        aws_access_key_id="AKIAI6QFCNIR42EGCCLA",
        aws_secret_access_key="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",
        region_name="us-west-2"
    )

    response = client.list_faces(CollectionId=collection_id,
                                 MaxResults=maxResults)



    while tokens:

        faces = response['Faces']

        for face in faces:
            response2 = client.compare_faces(SimilarityThreshold=80,
                                             SourceImage={
                                                 'S3Object': {
                                                     'Bucket': 'recogstore',
                                                     'Name': photo
                                                 }
                                             },
                                             TargetImage={
                                                 'S3Object': {
                                                     'Bucket': 'recogstore',
                                                     'Name': face['ExternalImageId']
                                                 }
                                             })
            res = not response2['FaceMatches']
            if  not res:
                count=count+1


        if 'NextToken' in response:
            nextToken = response['NextToken']
            response = client.list_faces(CollectionId=collection_id,
                                         NextToken=nextToken, MaxResults=maxResults)
        else:
            tokens = False
    if count == 0:
        send_Email()
    else:
        print("ไม่พบผู้ต้องสงสัย")
    return count


def delete_faces_from_collection(collection_id, faces):
    client = boto3.client(
        "rekognition",
        aws_access_key_id="AKIAI6QFCNIR42EGCCLA",
        aws_secret_access_key="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",
        region_name="us-west-2"
    )

    response = client.delete_faces(CollectionId=collection_id,FaceIds=faces)



    return len(response['DeletedFaces'])


def list_faces_in_collection(collection_id):
    maxResults = 2
    faces_count = 0
    tokens = True

    client = boto3.client(
        "rekognition",
        aws_access_key_id="AKIAI6QFCNIR42EGCCLA",
        aws_secret_access_key="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",
        region_name="us-west-2"
    )

    response = client.list_faces(CollectionId=collection_id,
                                 MaxResults=maxResults)



    while tokens:

        faces = response['Faces']

        for face in faces:
            print(face['ExternalImageId'])
            faces_count += 1
        if 'NextToken' in response:
            nextTok = response['NextToken']
            response = client.list_faces(CollectionId=collection_id,
                                         NextToken=nextTok, MaxResults=maxResults)
        else:
            tokens = False
    return faces_count

def getIdFace(Name):
    maxResults = 2
    faces_count = 0
    tokens = True

    client = boto3.client(
        "rekognition",
        aws_access_key_id="AKIAI6QFCNIR42EGCCLA",
        aws_secret_access_key="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",
        region_name="us-west-2"
    )

    response = client.list_faces(CollectionId=collection_id,
                                 MaxResults=maxResults)


    while tokens:

        faces = response['Faces']

        for face in faces:
            if face['ExternalImageId']==Name:
                return face['FaceId']

        if 'NextToken' in response:
            nextTok = response['NextToken']
            response = client.list_faces(CollectionId=collection_id,
                                         NextToken=nextTok, MaxResults=maxResults)
        else:
            tokens = False

def send_Email():
    client = boto3.client(
        "sns",
        aws_access_key_id="AKIAI6QFCNIR42EGCCLA",
        aws_secret_access_key="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",
        region_name="us-west-2"
    )
    response= client.publish(
        TopicArn = 'arn:aws:sns:us-west-2:599601063752:MySNS',
        Message = "พบผู้ต้องสงสัยบริเวณมหาวิทยาลัยธรรมศาสตร์"
    )



if __name__ == "__main__":

    faces=[]

    collection_id='Collection'
    bucket = 'recogstore'
    check=1
    while(check!=0):
        print("เลือกรายการตามต้องการ")
        print("1.เพิ่มรูปภาพนักศึกษาหรือบุคลากร")
        print("2.เพิ่มรูปภาพเพื่อตรวจหาบุคคลต้องสงสัย")
        print("3.ลบรูปภาพนักศึกษาหรือบุคลากร")
        print("4.แสดงชื่อรูปภาพทั้งหมด")
        print("0. เพื่อออกโปรแกรม")
        check = input("choice: ")
        if check=='1':
            print("กรุณากรอกชื่อรูปภาพ")
            photo = input()
            add_faces_to_collection(bucket, photo, collection_id)
        elif check=='2':

            print("กรุณากรอกชื่อรูปภาพ")
            photo = input()
            check_person(collection_id, photo)
        elif check=='3':
             print("กรุณากรอกชื่อรูปภาพ")
             Name= input()
             faces.append(getIdFace(Name))
             delete_faces_from_collection(collection_id,faces)
             print("Delete Success")
        elif check=='4':
            list_faces_in_collection(collection_id)
        elif check=='0':
            break















