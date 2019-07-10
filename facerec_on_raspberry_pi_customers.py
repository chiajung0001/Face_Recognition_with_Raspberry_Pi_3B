import face_recognition
import picamera
import numpy as np
import os
import time
import json
from confluent_kafka import Producer

#初始化
camera = picamera.PiCamera()
#設置相機解析度
camera.resolution = (320, 240)

output = np.empty((240, 320, 3), dtype=np.uint8)


print("Loading known face image(s)")


face_locations = []
face_encodings = []
face_names = []

known_person=[]
known_image=[]
known_face_encoding=[([-9.23262909e-02,  9.99013260e-02,  6.98956102e-02,  1.04054287e-02,
       -6.40720651e-02, -2.53240168e-02, -1.14967212e-01, -8.92674252e-02,
        1.02182008e-01, -6.90468326e-02,  2.45034441e-01, -3.08383517e-02,
       -2.40973696e-01, -9.68460515e-02, -1.64623521e-02,  1.88664764e-01,
       -1.96841970e-01, -8.41864049e-02,  5.48266806e-03,  1.81476958e-02,
        1.06988780e-01,  2.15717237e-02,  1.36812273e-02,  3.02001983e-02,
       -7.36223608e-02, -3.84128660e-01, -7.91088268e-02, -1.11284852e-01,
       -9.97055229e-03, -4.83401380e-02, -9.38500911e-02,  5.18499687e-02,
       -1.36307865e-01, -4.25032265e-02,  2.51051150e-02,  3.38767171e-02,
        9.05097090e-03, -2.34807711e-02,  2.02206388e-01,  3.67567539e-02,
       -2.18697309e-01,  3.71225700e-02,  3.78940161e-03,  2.06722617e-01,
        1.60588965e-01,  7.86168352e-02,  6.67275190e-02, -1.18395880e-01,
        9.52610075e-02, -1.65400222e-01,  1.26868309e-02,  1.70714542e-01,
        1.10528171e-01,  4.05438021e-02, -1.24149323e-02, -1.83318272e-01,
       -4.70876954e-02,  1.94638390e-02, -7.84706250e-02,  2.83120130e-03,
        6.34249374e-02, -7.15466738e-02, -8.32096487e-03, -7.76102990e-02,
        2.51626819e-01,  4.09594253e-02, -1.39343560e-01, -1.61878437e-01,
        7.90686309e-02, -8.96421298e-02, -1.18201114e-01,  3.94128226e-02,
       -1.82324156e-01, -1.52014419e-01, -3.23631972e-01,  3.90087292e-02,
        3.69437546e-01,  3.18823867e-02, -2.04149604e-01,  4.63549644e-02,
       -1.15051992e-01, -2.25507542e-02,  8.88231769e-02,  1.57751769e-01,
        1.62774697e-04,  1.50351366e-02, -4.93859760e-02, -3.19266543e-02,
        2.05339342e-01, -9.61916745e-02, -2.03587580e-02,  1.92843214e-01,
       -2.60992497e-02,  1.77982792e-01, -1.60332210e-02,  1.59724597e-02,
       -2.43471768e-02,  4.30353135e-02, -5.85169569e-02,  2.02979241e-02,
        2.90793143e-02, -2.92942561e-02,  2.07778774e-02,  1.09181404e-01,
       -1.77399814e-01,  5.76695092e-02,  9.76321986e-04,  5.59044816e-02,
        6.53192475e-02,  6.94294348e-02, -1.59347981e-01, -9.41510424e-02,
        1.21973105e-01, -2.51387388e-01,  2.25581855e-01,  2.11473376e-01,
        5.39765246e-02,  8.68209600e-02,  1.46954715e-01,  9.62193087e-02,
       -1.75283831e-02,  1.21255582e-02, -2.18175814e-01, -2.51578260e-02,
        1.32805422e-01,  1.52771492e-02,  1.17169637e-02, -2.09619477e-03]), 
        ([-1.61472902e-01,  7.08273947e-02,  5.37359640e-02, -5.28303608e-02,
       -6.93021417e-02,  9.41903796e-03, -7.43949041e-02, -1.32346109e-01,
        7.42695406e-02, -9.54875275e-02,  2.19931111e-01, -6.15128316e-02,
       -2.46706590e-01, -9.01269391e-02, -3.76338437e-02,  1.79550603e-01,
       -2.01655120e-01, -1.17141090e-01, -2.98182853e-03,  7.16278851e-02,
        1.02216586e-01, -3.69981453e-02, -6.85350299e-02,  4.46557701e-02,
       -1.26060352e-01, -3.28970104e-01, -7.60806352e-02, -4.18842137e-02,
       -2.43166797e-02, -2.97233332e-02, -5.52231669e-02,  2.52428818e-02,
       -2.13707238e-01, -1.94528084e-02, -1.10911727e-02,  7.27141574e-02,
        1.74437016e-02,  1.30350022e-02,  1.51983410e-01,  1.89155638e-02,
       -2.41971225e-01,  3.70627977e-02,  6.09459579e-02,  2.46739253e-01,
        1.66121796e-01,  4.69499715e-02,  2.06509270e-02, -1.32211968e-01,
        1.11703590e-01, -2.24889696e-01,  5.66780195e-02,  1.36864036e-01,
        1.27257407e-01,  7.41422698e-02, -6.40763864e-02, -1.35443717e-01,
        3.11132763e-02,  9.62302983e-02, -1.97161272e-01,  1.46733224e-01,
        1.39825985e-01, -1.42933398e-01,  1.59386545e-05, -4.75695468e-02,
        2.01885775e-01,  4.54983786e-02, -1.51455969e-01, -1.66964546e-01,
        9.54916403e-02, -1.23806238e-01, -7.48224258e-02,  2.91730836e-02,
       -1.18734680e-01, -2.40150675e-01, -3.97014529e-01,  6.79534674e-02,
        3.50239664e-01,  1.67940095e-01, -2.19147578e-01,  3.75162661e-02,
       -7.02899396e-02, -3.25852819e-02,  1.37502924e-01,  1.61233574e-01,
        1.27920359e-02,  2.04286501e-02, -7.94796571e-02,  3.99264619e-02,
        2.47765720e-01, -2.92355567e-02,  1.02497544e-02,  2.86946058e-01,
        1.30558927e-02,  5.32834083e-02, -2.12320015e-02,  8.74235183e-02,
       -5.63837923e-02, -1.85287232e-03, -1.13245830e-01, -6.84050517e-03,
        1.34484619e-02, -5.17437905e-02,  6.56010360e-02,  1.22180797e-01,
       -1.70910284e-01,  1.73425019e-01, -3.49702593e-03,  4.67811301e-02,
        1.95517391e-02, -1.01258000e-02, -1.17236130e-01, -6.13239035e-02,
        1.17506877e-01, -2.03539446e-01,  2.09779203e-01,  1.89400777e-01,
        1.46461248e-01,  8.67860988e-02,  1.51608929e-01,  6.13147542e-02,
        7.24592898e-03, -2.03579590e-02, -1.74106851e-01, -1.19233932e-02,
        1.12980805e-01, -4.36122529e-02,  1.32703885e-01,  4.73235957e-02]), 
        ([-0.04116528,  0.04281201,  0.07165854,  0.07454566, -0.03375656,
       -0.05049718, -0.01858589, -0.14537051,  0.14282067, -0.04792278,
        0.25440249, -0.09327017, -0.19685453, -0.14655188, -0.0146217 ,
        0.18585838, -0.11818407, -0.05797022, -0.04583003, -0.00633837,
        0.08078568, -0.03136272,  0.09402596,  0.07956349, -0.04075776,
       -0.38406721, -0.13345264, -0.14762898,  0.01722859, -0.06676294,
       -0.07619423,  0.07091655, -0.13344501, -0.11021597, -0.01223277,
        0.04745333, -0.04227641, -0.08579283,  0.20445728, -0.09443976,
       -0.20771891, -0.01523468,  0.04048155,  0.19764408,  0.17776148,
        0.0863634 ,  0.04538983, -0.10874002,  0.11223935, -0.08512405,
        0.04305754,  0.11862573,  0.07654982,  0.03977791, -0.01122959,
       -0.12285286,  0.01454058,  0.08126725, -0.14699966, -0.01007161,
        0.04520166, -0.09366044, -0.03478969, -0.01958942,  0.17950186,
        0.07686316, -0.04796101, -0.16970664,  0.12878247, -0.18627891,
       -0.04381437,  0.05165909, -0.21186221, -0.18942925, -0.33792958,
       -0.02118361,  0.37212169,  0.02310716, -0.18181555,  0.03114656,
       -0.03535907,  0.00869491,  0.14584886,  0.16664779,  0.02277142,
       -0.00431657, -0.14597541, -0.03906627,  0.16627835, -0.11607608,
       -0.03424564,  0.18795836, -0.01790763,  0.04290415,  0.02873446,
        0.03301659, -0.03973429,  0.08764086, -0.13412262, -0.00904232,
        0.09090219,  0.02430574, -0.00885418,  0.05077478, -0.15526882,
        0.07850194,  0.01558722,  0.06293024,  0.07411676, -0.05607088,
       -0.15352151, -0.09914742,  0.17930089, -0.17230622,  0.14119017,
        0.15926257,  0.02761899,  0.11654088,  0.07646608,  0.160019  ,
       -0.03195654, -0.03969917, -0.25953507,  0.0310539 ,  0.13198848,
        0.02009649,  0.03177908, -0.00113958]), 
        ([-0.15924892,  0.17058739,  0.03511739, -0.02322692, -0.12720005,
       -0.08774094, -0.06840292, -0.15342224,  0.12838231, -0.05368762,
        0.21129248, -0.0605409 , -0.18470071, -0.14801177, -0.00504731,
        0.18689679, -0.18794231, -0.15023929,  0.01218005, -0.02153865,
        0.07270315, -0.00933455,  0.05898435,  0.06446709, -0.13606513,
       -0.36964482, -0.05930848, -0.12359036,  0.06014783, -0.01689517,
       -0.07832025,  0.0584035 , -0.21244183, -0.12503907,  0.06242119,
        0.1084258 ,  0.0157525 ,  0.00455744,  0.18234447, -0.04299523,
       -0.24056567, -0.03529577,  0.10272295,  0.27727261,  0.18130626,
        0.02448086,  0.07469895, -0.13439472,  0.09220486, -0.08304353,
        0.07133128,  0.14719792,  0.07899825,  0.05015311, -0.03958188,
       -0.14077398,  0.00410662,  0.14414057, -0.18943298,  0.06559266,
        0.16631085, -0.07622393, -0.07815373, -0.05863765,  0.29829878,
        0.06158252, -0.13253883, -0.18547392,  0.11471903, -0.13503386,
       -0.05526519,  0.04634846, -0.16854675, -0.16873537, -0.31282547,
        0.01701349,  0.33439454,  0.07676975, -0.17272797,  0.06269702,
       -0.07815578, -0.01447407,  0.11436969,  0.1900546 ,  0.00875077,
        0.0603455 , -0.05006285,  0.01780038,  0.20354623, -0.05253609,
        0.00738153,  0.22743428, -0.00460277,  0.04237384,  0.00224294,
        0.03788062, -0.0951854 ,  0.03203173, -0.12844962, -0.03395026,
        0.02101853, -0.06828438,  0.02435065,  0.09684279, -0.18828489,
        0.07941162,  0.02543302,  0.08895875,  0.02114782, -0.02493188,
       -0.07273676, -0.14540695,  0.13122961, -0.19590881,  0.25464195,
        0.18893535,  0.07592543,  0.13267867,  0.13009956,  0.08004983,
        0.05543999, -0.02124308, -0.15236843,  0.03484788,  0.12002655,
       -0.08889764,  0.10279807,  0.01933774]), 
       ([-0.16937481,  0.01319485,  0.02962789,  0.01842855, -0.02302701,
       -0.09753657, -0.08388496, -0.08983038,  0.10613733, -0.03438269,
        0.23969677, -0.05468694, -0.13523029, -0.16153334,  0.02142633,
        0.16564712, -0.21778591, -0.09791851,  0.02588722, -0.04417749,
        0.06785791, -0.0655389 ,  0.00178977,  0.14485179, -0.13109019,
       -0.39624697, -0.08520737, -0.18295085,  0.03291597, -0.0464569 ,
       -0.04421508,  0.0516592 , -0.13788173, -0.07570626,  0.04497258,
        0.1226281 ,  0.03861415, -0.04557427,  0.2189413 , -0.05125177,
       -0.18332742,  0.01064432,  0.10230522,  0.2609739 ,  0.18559583,
        0.07021338,  0.04782303, -0.02392053,  0.12867741, -0.18437751,
        0.05537139,  0.13451274,  0.11975583,  0.02709238,  0.04714632,
       -0.13797455,  0.00968102,  0.10014313, -0.19871065,  0.08315216,
        0.03050929, -0.07889174,  0.01333835, -0.00194244,  0.26678863,
        0.09756772, -0.13605964, -0.06671172,  0.15813045, -0.13955772,
       -0.05794697, -0.0010939 , -0.15329018, -0.22086263, -0.36153382,
        0.05072775,  0.36194342,  0.11925844, -0.19114122,  0.08894955,
       -0.07320996, -0.0182673 ,  0.11133053,  0.12361977, -0.02744335,
       -0.02060747, -0.07667311, -0.01064095,  0.19791031,  0.04615999,
        0.00293272,  0.19284309, -0.02306863,  0.0390658 ,  0.02671893,
        0.03575907, -0.04836994, -0.01990625, -0.13083501, -0.00710493,
        0.04599701, -0.04283249,  0.05010497,  0.08458614, -0.25110251,
        0.02940882,  0.03056192, -0.00679725,  0.01903611,  0.0863857 ,
       -0.16225691, -0.05402782,  0.13103509, -0.25407478,  0.23152897,
        0.21215375,  0.11183234,  0.16067956,  0.10634831,  0.02773244,
        0.013109  , -0.0744089 , -0.14272666, -0.01569472,  0.07280301,
       -0.0116183 ,  0.07997784,  0.05375577])]


# 創建一個名為"customers"資料夾並從裡面的會員人臉抓取人臉特徵並以檔案名稱為人臉名稱
for file in os.listdir("customers"):
    try:
        known_person.append(file.replace(".jpg", ""))
        file=os.path.join("customers/", file)
        known_image = face_recognition.load_image_file(file)
        known_face_encoding.append(face_recognition.face_encodings(known_image)[0])
    except Exception as e:
        pass



while True:
    print("Capturing image.")
    #從相機抓取一幀圖像轉為numpy陣列
    camera.capture(output, format="rgb")

    # 找出當前視頻中所有的人臉及臉部編碼
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # 循環檢查框架中的人臉是否為已知的會員人臉
    for face_encoding in face_encodings:
        props={'bootstrap.servers':'10.120.28.3:6667'}
        p = Producer(props)
        match = face_recognition.compare_faces(known_face_encoding, face_encoding, tolerance=0.45)
        matches=np.where(match)[0] #檢查哪個圖片是符合的
        if len(matches)>0:
          name = str(known_person[matches[0]])
          member_detail = {"memberID" : name} 
          member_detail_json = json.dumps(member_detail).encode("utf-8") 
          p.produce('facein', value=member_detail_json)
        else:
          name = "Unknown"

        print("I see someone named {}!".format(name), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))




