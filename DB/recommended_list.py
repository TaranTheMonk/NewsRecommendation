from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RecommendedList(Base):
    __tablename__ = "recommended_list"

    def __init__(self, device_id, recommended_list):
        self.device_id = device_id
        self.recommended_list = recommended_list

    device_id = Column(String, primary_key=True)
    recommended_list = Column('list', String)


def insert_recommended_list(session, recs, bulksize=100):
    if len(recs) > bulksize:
        insert_recommended_list(recs[bulksize:], bulksize)
        recs = recs[:bulksize]
    if len(recs) == 0:
        return
    sqlb = "INSERT INTO recommended_list (device_id, list) VALUES "
    sqldata = ','.join("('%s', '%s')" % (rec.device_id, rec.recommended_list) for rec in recs)
    sqle = " ON DUPLICATE KEY UPDATE list=values(list)"
    session.execute(''.join([sqlb, sqldata, sqle]))
    session.commit()


def insert_rec_from_file(session, file_path, bulksize=100):
    file = open(file_path, 'r')
    recs = []
    for line in iter(file.readline, ''):
        sp = line.split('\t', 1)
        if len(sp) == 2:
            recs.append(RecommendedList(sp[0], sp[1]))
        if len(recs) == bulksize:
            insert_recommended_list(session, recs, bulksize)
            recs = []
    insert_recommended_list(session, recs, bulksize)
    file.close()


# def rec_test():
#     db_engine = create_engine(
#         'mysql://HSDBADMIN:NestiaHSPWD@hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com:3306/news')
#     session = sessionmaker(bind=db_engine)()
#     recs = [RecommendedList("chinese",
#                             '[[367,8880,528,75,565,544,51,126,49,534,198,8845,407,450,158,179,490,141,100,347,8857,59,484,549,8921,75,426,133,520,513,8897,587,75,435,89],[578,336,8924,161,118,532,513,370,8889,562,8918,580,573,478,471,605,539,518,153,431,493,457,436,188,8842,569,451,485,203,8888,340,493,190,496,112],[95,373,474,204,153,507,588,8881,493,535,533,189,418,40,429,534,38,104,158,518,8886,105,572,560,143,58,519,137,551,190,183,8921,459,8890,471],[8851,381,91,8901,460,520,422,76,8911,436,387,608,186,448,115,150,8855,427,386,451,464,560,566,525,100,532,448,39,104,8865,454,8845,100,535,463],[173,342,421,361,8907,386,8886,526,179,341,583,492,588,352,202,156,567,50,344,164,341,151,50,8898,327,555,8871,386,514,375,101,337,383,402,338],[88,433,473,8869,8870,492,490,347,38,588,458,516,532,171,152,82,44,530,511,509,582,537,473,510,387,148,428,497,8861,454,8891,154,435,380,541],[8871,8859,8864,532,540,8867,204,204,184,190,146,468,571,8841,8866,488,8901,8855,44,131,8854,100,177,377,155,557,430,457,537,561,476,562,365,211,484],[95,8862,498,76,342,512,40,144,8888,326,134,130,8901,164,578,428,150,8909,190,454,212,533,154,353,140,582,337,104,8923,152,351,171,65,407,488],[116,530,479,49,586,165,8916,126,402,428,104,8845,191,79,346,461,126,407,8911,388,8906,123,8909,206,524,64,480,606,555,480,40,8897,454,91,202],[48,533,504,198,387,8865,128,154,104,119,483,161,8902,157,434,134,77,346,452,380,82,202,202,8901,96,8845,8897,157,8879,370,77,420,180,206,348],[154,57,200,526,42,189,403,143,42,134,8850,157,111,605,112,492,468,204,136,573,152,338,8899,77,8918,569,59,8913,134,585,8918,135,485,128,8865],[526,482,8888,65,468,407,8880,418,479,435,131,429,8909,131,429,208,8884,367,216,589,427,8879,8872,441,492,375,517,138,560,8890,161,8861,537,131,604],[197,520,513,136,212,483,53,571,8880,380,536,145,99,196,202,449,124,8841,8892,65,504,563,97,8906,438,427,179,210,516,191,8878,8885,116,181,8864],[431,152,327,577,41,488,448,145,493,8889,49,4846,53,333,529,59,568,91,572,176,162,8889,115,510,462,386,418,84,8892,200,468,8859,569,449,357],[74,345,38,475,8852,481,8862,8845,8913,510,133,154,212,514,56,75,8919,193,563,586,83,8901,553,118,111,347,211,8853,163,112,557,357,567,350,116],[453,586,8910,206,379,578,8842,8850,541,426,546,8877,93,8921,192,8877,8876,8924,459,506,197,138,109,45,420,8877,8907,583,174,67,107,381,387,422,577],[447,520,480,585,538,588,8899,84,8844,8923,212,8900,52,44,604,467,176,67,162,92,154,70,631,456,83,525,142,573,8855,8849,520,99,163,519,460],[8861,8856,526,48,343,150,140,498,457,458,8911,46,431,8917,496,343,192,361,386,546,8864,143,331,8878,467,363,135,189,375,161,370,90,402,8906,529],[450,485,165,205,353,607,387,531,351,163,381,180,456,149,338,136,152,181,354,92,8878,454,579,333,464,606,566,526,38,8868,116,461,588,502,53],[338,51,8872,546,98,188,540,8878,8910,150,75,98,8882,8901,421,8847,564,8866,165,468,354,67,154,121,208,194,528,429,198,346,8877,388,173,205,346],[433,98,429,8917,345,374,157,495,110,201,561,102,8876,94,377,72,438,137,8919,8906,8892,132,336,542,146,526,59,89,8909,551,8847,8891,131,8909,182],[428,557,491,460,8841,569,8860,8850,420,420,344,8898,455,507,347,134,151,500,334,574,326,8895,551,588,173,584,8864,515,361,57,43,8850,159,363,428],[575,8902,8922,79,533,495,549,119,379,375,580,113,8872,477,448,488,56,566,498,569,377,514,189,43,551,51,163,8847,459,90,155,8922,8856,90,346],[424,130,544,8846,109,8908,114,8854,106,348,74,173,444,131,76,364,550,8911,157,186,87,135,172,192,152,182,326,8924,88,108,148,8915,122,8886,152],[450,72,206,387,96,555,327,40,197,544,44,8856,607,538,185,424,459,557,183,49,186,148,50,383,74,98,72,518,86,357,480,465,565,443,57],[67,564,8903,8910,563,430,4846,59,175,8911,8883,529,407,460,589,343,190,8843,48,324,576,8904,8914,8870,43,453,328,162,194,87,152,606,334,8914,58],[53,537,187,72,92,180,4846,341,558,333,335,326,102,480,586,542,8854,60,478,8920,350,569,420,39,103,508,569,150,383,365,361,582,586,160,59],[379,80,513,491,8904,351,38,459,8891,507,147,175,604,79,335,438,577,168,582,427,103,434,163,109,487,530,418,499,533,70,534,564,499,8851,131],[534,103,91,342,537,532,431,369,8858,107,8914,388,164,111,96,60,8876,187,138,108,185,88,8882,8899,8875,8912,402,161,350,580,475,8911,8892,174,563],[326,95,453,79,561,8879,131,170,67,8891,631,586,536,508,141,444,119,419,363,500,128,8874,559,151,462,462,571,56,455,574,447,105,8900,331,369],[101,474,460,524,93,457,432,57,110,585,511,429,173,526,51,86,47,8901,462,383,379,419,102,65,499,8851,578,73,8861,175,89,98,335,8872,8879],[429,186,8868,118,211,380,102,504,185,92,431,174,8912,94,135,386,120,364,571,137,8913,559,196,374,8897,8843,8904,8878,109,330,90,170,133,183,92],[572,76,105,327,191,518,8854,55,443,195,568,64,464,91,585,8914,8887,8853,452,8879,334,474,116,95,176,213,373,8896,459,216,432,488,79,537,462],[73,327,8864,419,407,564,150,8894,388,575,193,587,428,70,121,334,138,352,92,72,528,193,64,578,374,40,339,491,8887,567,456,120,8895,8902,161],[8900,8841,73,477,109,471,58,402,8845,92,546,568,8856,172,68,99,345,207,380,340,334,47,45,70,185,578,8865,67,573,100,555,8899,8844,496,8917],[75,427,84,345,473,8863,195,365,490,163,8845,407,56,204,331,138,124,353,569,127,514,8899,438,477,189,383,156,8916,447,348,107,427,145,158,182],[8841,354,8897,556,117,164,47,8862,147,190,8898,8848,441,199,8915,157,515,589,526,8915,146,161,381,534,422,421,328,136,102,475,346,508,127,8905,47],[354,41,160,98,188,51,68,540,38,55,8841,374,565,181,39,202,498,45,347,38,579,8869,105,509,497,64,8845,429,501,336,455,501,502,208,429],[566,211,418,535,142,8852,347,402,44,606,8885,381,8908,137,539,181,419,41,537,154,118,209,525,504,171,501,8881,88,203,8895,169,8890,199,39,8853],[370,128,428,8918,8896,345,113,141,8884,343,8864,8867,470,448,557,38,564,464,119,98,8908,475,572,8852,568,336,8844,196,604,364,567,107,329,201,569],[60,166,8904,44,8871,105,587,51,8911,334,455,8901,39,126,8882,8917,159,8855,98,186,523,8911,354,579,562,8861,333,38,341,205,544,338,128,456,424],[8857,534,520,181,587,478,587,333,216,216,205,8893,143,211,170,105,8873,133,329,40,454,500,333,43,8911,504,163,208,99,124,212,150,58,587,76],[8895,8875,631,579,56,454,189,510,182,572,8864,96,70,560,8912,478,350,589,144,443,200,210,50,352,353,8923,56,8921,330,198,540,331,8909,361,184],[196,156,344,605,202,212,354,482,491,120,42,604,607,8913,162,471,530,139,179,498,201,8884,585,425,153,605,55,41,519,84,113,550,129,46,98],[8864,204,463,538,72,8919,329,47,50,381,64,203,59,8877,434,528,169,434,421,449,103,331,348,528,73,161,8901,116,141,172,504,488,53,116,8884],[377,487,202,8883,86,70,8903,535,87,8866,8858,140,535,8881,475,443,8907,197,460,174,8910,572,326,495,8873,577,377,456,169,168,179,367,429,8894,8890],[350,435,338,8922,539,8919,476,8879,8863,348,178,73,480,8862,8875,324,338,125,360,126,564,169,216,517,496,473,143,332,144,512,8894,153,549,185,8871],[55,407,467,160,440,106,189,172,105,190,456,481,8848,119,565,371,458,8889,8876,8864,379,483,88,8864,42,67,216,8854,523,142,105,85,207,147,8888],[530,146,151,201,493,8863,68,487,536,495,558,44,588,8913,379,470,560,631,8917,49,8880,94,377,8921,324,176,210,463,44,109,60,419,334,204,103],[365,8883,584,184,8847,207,202,8909,338,528,87,402,574,490,329,561,8892,504,92,8875,8866,363,8892,43,582,562,479,60,383,210,216,183,52,558,377],[327,464,555,196,59,491,541,88,607,92,100,574,138,534,149,101,431,579,149,471,383,566,162,102,8868,499,478,179,105,512,429,8863,496,176,85],[8921,76,122,343,53,555,206,345,209,155,567,110,134,568,474,8923,158,605,380,101,371,332,589,8880,134,67,79,152,8870,526,498,94,64,490,337],[528,8893,160,447,8923,353,44,8857,497,89,562,83,483,153,379,631,8866,8893,127,336,330,73,538,551,509,329,109,545,493,504,92,85,212,40,406],[8877,39,204,536,132,8850,8891,544,500,128,125,380,537,39,195,93,577,563,345,8891,572,130,142,102,468,365,8885,123,84,197,80,8913,444,8851,64],[144,213,8877,509,166,198,377,8883,44,126,555,374,142,568,100,403,8912,170,501,8886,332,8856,418,336,8918,43,186,8844,518,93,8917,160,190,491,363],[444,326,214,334,540,406,452,8883,531,588,173,42,157,351,531,342,528,8857,386,8846,402,90,552,138,512,115,8889,144,126,149,449,126,575,8842,208],[164,8910,8865,165,541,560,8884,199,99,77,8841,8845,80,83,484,60,450,573,352,458,418,48,488,8889,73,440,526,104,587,86,8902,45,345,451,94],[607,568,77,8885,342,470,64,557,8868,188,473,8860,456,558,8923,456,8877,440,455,155,495,375,8877,8886,185,140,166,59,485,352,375,152,546,138,111],[8866,462,8907,426,574,140,506,8896,431,183,202,196,364,573,57,449,443,403,364,473,507,422,483,364,82,8915,452,144,422,8860,449,345,470,8914,546],[50,8890,8866,492,420,187,8892,454,148,178,148,444,514,206,138,137,8899,207,216,203,104,168,122,558,572,585,137,8916,94,208,73,70,8894,575,508],[176,513,87,582,525,474,122,576,588,374,324,80,194,485,386,435,518,488,345,207,204,578,510,434,430,200,8859,515,476,606,153,8897,434,216,201],[145,402,477,608,79,8917,86,383,364,8904,572,436,587,542,561,436,582,462,606,452,587,452,8916,46,496,55,213,556,403,418,8922,134,8918,535,8862],[479,526,50,528,481,346,501,327,86,490,48,121,330,480,134,339,402,58,468,485,8885,117,464,132,456,147,141,465,424,529,441,169,525,8856,434],[450,473,473,202,124,96,525,473,8850,134,583,8924,8858,479,421,549,8880,165,556,363,529,135,97,481,331,163,199,539,506,561,187,354,386,41,175],[8923,558,510,501,631,8875,557,116,175,168,520,8885,477,463,479,8858,373,586,8845,461,8859,96,501,456,8855,462,184,455,8914,184,469,340,8858,583,562],[148,425,214,8898,196,153,8899,552,159,8854,557,83,8888,373,523,8849,451,123,167,8862,562,156,572,386,500,534,511,199,492,333,8899,106,524,189,538],[450,8865,130,528,8871,374,433,87,496,435,351,123,496,123,178,8877,173,51,193,432,144,128,8901,490,581,588,8904,388,462,129,8913,434,8909,207,387],[460,490,501,353,132,105,531,459,421,8913,85,353,536,532,8922,88,581,336,431,180,584,140,77,8847,166,158,8922,571,340,370,8886,328,564,8902,347],[8876,526,86,463,216,370,8865,8911,335,185,8874,422,204,44,457,515,454,158,518,8865,492,360,465,8913,557,8871,8900,199,72,8873,65,8894,438,216,8873],[327,154,43,374,211,182,341,333,153,8850,580,140,153,206,340,433,494,65,512,146,8912,127,154,526,342,8841,571,183,83,151,139,524,8912,83,208],[90,207,8918,119,8869,483,159,8876,86,363,512,512,100,8887,91,172,8913,338,563,8888,607,175,386,8917,468,528,578,151,8890,202,479,169,452,181,424],[192,349,496,193,122,454,8886,125,190,58,91,340,506,509,88,568,383,535,538,157,200,353,419,216,498,8847,553,562,470,490,8878,122,588,561,8844],[449,169,8869,473,211,8863,516,133,94,326,350,8865,534,151,80,496,8864,8895,542,143,8854,578,127,136,158,8870,88,116,8880,210,361,335,342,8892,523],[8890,8878,8923,173,8877,89,517,8841,42,8888,480,483,551,198,542,48,580,333,149,8916,367,186,606,335,607,326,436,564,82,163,144,8853,8912,83,105],[44,185,57,94,8877,357,8858,156,438,180,464,350,8893,470,8856,403,45,326,8855,188,8904,8862,567,370,75,538,8900,46,380,111,134,511,351,471,139],[403,339,129,205,388,192,546,68,195,101,473,165,573,8909,573,465,147,379,423,452,8870,185,336,157,604,440,8921,457,354,569,438,115,490,8893,407],[346,77,8871,57,189,8844,8867,87,76,104,8843,339,430,454,189,135,75,507,608,93,118,206,96,135,480,402,123,532,8888,469,8915,339,407,457,125],[102,8924,160,476,583,8896,529,379,465,460,8843,190,93,499,8864,47,324,478,8918,452,91,111,475,174,8923,135,454,8860,571,8905,8924,428,8843,8921,428],[347,477,568,104,197,192,552,199,4846,92,216,85,558,180,8863,178,516,460,573,160,172,8870,540,549,519,166,504,43,93,474,60,8857,467,88,8877],[134,8895,83,73,557,101,107,532,459,70,42,130,369,44,374,575,8906,508,402,92,369,136,500,518,114,343,453,8844,490,8884,379,586,172,496,156],[8914,169,135,493,65,587,438,481,427,456,582,154,561,361,8911,100,214,209,463,520,480,535,563,56,159,8922,351,41,365,568,206,538,474,8874,577],[353,335,127,8889,193,8915,79,46,68,164,8923,94,8915,582,460,373,140,538,541,517,52,8900,447,104,59,450,179,477,77,91,8865,173,566,113,94],[340,8916,8854,8861,468,8882,8865,55,8864,419,571,144,440,375,8847,536,569,8879,168,523,168,190,8868,171,470,8862,8862,56,494,123,59,608,8843,118,423],[106,8903,354,157,135,8924,8903,198,189,428,329,139,84,324,406,524,553,8861,506,84,582,8898,132,184,575,336,8841,8917,180,93,139,121,434,487,363],[192,383,8890,579,402,77,549,8873,193,54,480,178,514,331,475,447,331,202,573,200,581,8877,171,344,91,577,119,168,434,335,214,8867,136,111,567],[8878,364,586,8841,525,95,83,581,8924,100,453,39,60,578,151,568,160,60,74,435,8857,518,379,90,373,371,454,123,8905,367,57,8924,455,559,8882],[8882,459,8917,190,47,587,128,8888,8843,585,443,172,149,427,428,573,80,8907,169,48,159,455,8915,8857,531,8884,89,47,607,8919,557,8870,541,183,324],[331,8905,8869,334,403,106,157,508,73,452,551,4846,587,581,580,343,456,562,164,60,438,60,467,100,8885,585,550,98,460,168,8897,116,8861,80,8918],[136,80,8851,465,73,519,330,464,333,8879,160,70,8919,493,8895,74,141,582,438,476,194,418,386,207,210,156,8917,116,425,532,422,121,506,344,123],[332,184,532,551,380,459,344,76,149,40,73,115,142,8878,8845,100,85,440,607,82,187,364,102,211,8911,476,148,205,8865,8887,127,524,353,186,60],[154,545,326,386,214,54,589,8865,533,123,8847,453,144,572,8884,566,123,176,113,185,511,453,569,508,452,117,8863,102,8885,203,506,149,497,8880,571],[540,102,8863,427,8903,571,488,528,108,537,457,332,536,86,8917,8875,136,606,161,516,430,467,517,151,535,90,79,8882,8894,365,336,532,360,8895,420],[203,8919,210,454,8881,551,435,576,584,343,438,8911,348,131,528,147,8866,45,428,145,133,498,469,490,166,572,436,8895,100,8875,182,8912,127,343,80],[49,589,161,114,123,402,454,212,435,8858,475,116,447,8890,459,96,343,8870,197,159,8851,531,8866,363,98,91,64,538,8914,142,586,347,578,563,8874],[545,353,171,532,8907,112,528,88,123,121,104,363,562,159,584,465,165,498,482,119,476,8915,353,510,478,8904,122,334,209,456,8862,448,129,172,363],[444,517,205,8869,181,128,211,579,8880,8917,210,565,380,546,351,533,59,152,108,513,8892,513,494,50,427,566,8899,171,387,499,490,353,201,123,532],[8878,513,572,8871,77,534,607,8917,444,334,421,351,335,8859,461,443,85,82,327,179,539,457,191,517,482,171,8856,454,8900,456,124,363,8879,562,508],[557,326,45,484,8914,357,608,8875,440,211,116,511,68,462,155,558,344,333,544,357,8850,354,195,43,354,383,173,122,139,75,450,111,463,555,122],[8883,8896,120,8859,457,508,110,8860,383,213,577,447,545,508,199,529,467,107,8847,425,128,576,201,212,605,50,386,8841,8884,8844,471,125,478,542,114],[351,581,8855,8848,8911,334,131,383,124,459,8904,8905,72,422,52,111,346,148,469,98,337,49,142,480,147,8869,332,585,93,8874,488,8845,576,504,39]]'),
#             RecommendedList("english",
#                             '[[518,631,523,8908,513,8885,364,186,460,8886,58,8897,481,8866,42,364,145,140,512,191,402,373,572,8853,589,8909,149,461,112,97,357,337,488,605,140],[60,462,580,573,159,8878,200,326,465,170,569,8895,191,8841,421,462,580,205,8900,559,124,198,8881,56,8917,8916,558,130,380,183,387,352,140,8858,193],[175,419,551,70,8893,185,8881,211,141,138,8876,174,531,587,138,569,108,59,209,128,361,210,115,8878,111,141,607,369,90,79,440,42,430,501,8866],[631,201,8875,520,45,541,8874,8851,338,38,203,55,170,178,449,79,463,424,488,332,113,453,167,506,75,129,330,564,508,72,98,197,198,519,488],[84,493,131,117,8862,8903,8906,8852,120,202,451,8842,65,8884,177,448,8923,94,135,340,351,73,338,553,146,511,343,8922,357,50,51,330,383,559,8858],[179,330,174,379,493,500,572,8846,8880,184,335,461,459,386,100,520,212,8868,105,105,8884,487,149,572,8888,334,205,67,184,532,8923,8866,553,8854,195],[8847,329,406,499,544,199,176,92,162,130,185,8871,434,151,8899,589,8916,499,480,537,86,523,171,40,328,482,448,557,112,536,515,456,152,530,456],[528,205,190,388,82,8891,83,180,8843,100,582,8904,560,457,142,352,440,171,341,420,8882,8859,564,490,504,475,188,65,169,8850,60,103,500,419,388],[332,456,367,474,552,96,531,8863,431,530,493,96,8857,203,407,528,8868,8869,178,55,432,8912,585,8866,571,141,133,520,585,463,214,160,8841,171,345],[8888,383,571,8862,460,174,429,151,8862,480,75,8868,425,334,130,352,8912,432,338,348,8864,576,8907,571,403,556,193,563,8889,564,534,553,8843,119,203],[365,77,8847,121,544,8902,454,8924,8853,329,50,158,403,474,182,166,8862,578,504,8907,148,168,536,52,524,470,128,467,8847,51,87,607,110,495,561],[99,75,177,449,332,59,469,8914,144,487,353,48,335,210,140,374,173,8853,100,128,364,157,48,48,184,212,118,499,485,8849,8865,73,8920,142,352],[8843,8884,204,8869,423,44,211,56,8877,565,118,85,46,203,347,60,8896,192,324,8884,159,41,8919,8848,501,458,161,8859,587,429,44,386,495,199,45],[8857,128,8854,402,92,8861,75,116,510,577,162,349,422,475,59,213,8908,59,556,577,216,76,204,8874,478,147,438,538,369,8896,146,464,438,115,451],[485,8887,77,77,53,154,8911,8876,8858,108,561,104,353,67,114,492,76,8862,144,8878,8916,475,562,149,206,520,188,564,326,185,373,579,516,8910,452],[192,8861,110,111,96,537,40,381,331,55,529,179,8898,448,480,8878,74,156,420,8857,475,606,205,589,456,8905,8886,165,88,500,588,8863,468,185,187],[8855,512,559,8919,329,207,75,54,459,43,425,8854,73,482,162,351,580,8911,8907,72,480,208,402,8902,363,339,431,132,147,126,8871,517,55,329,450],[354,8856,516,604,388,171,491,552,163,455,586,540,85,529,72,449,354,8923,127,490,8887,374,585,162,8896,535,124,333,509,8869,423,402,134,343,194],[8853,168,205,162,587,150,187,545,506,407,138,374,42,337,60,84,174,470,434,116,562,538,584,499,553,463,545,8886,431,44,153,8872,117,328,89],[494,137,140,123,140,374,164,517,8865,402,537,360,374,441,467,530,462,139,8863,100,8849,589,555,565,565,341,43,584,8905,464,528,515,447,8911,428],[8896,56,8905,468,108,545,347,451,515,65,8902,157,553,130,8878,514,8856,8906,373,87,8858,587,8850,512,204,8881,402,87,353,517,383,8854,159,346,198],[585,545,462,494,125,111,166,120,525,8877,199,8905,8859,8916,163,423,566,118,580,8912,8861,576,87,507,492,57,357,79,145,497,169,387,72,8878,216],[156,77,581,115,101,380,529,127,8921,112,485,523,583,213,8859,142,373,8915,370,110,171,172,526,43,8900,558,531,148,175,210,169,171,48,193,8846],[8849,8881,50,51,8899,8853,8847,479,334,345,532,347,531,8906,8876,471,440,421,8851,495,428,172,8893,529,8921,586,160,542,367,8878,8901,186,379,48,8897],[56,448,490,501,476,142,8883,436,8911,44,171,434,560,453,169,8897,52,216,84,585,492,201,8906,8850,47,139,470,8906,459,552,73,183,333,556,8914],[208,8875,109,93,328,8904,443,97,170,73,418,163,481,83,8873,334,8914,60,38,504,8873,206,428,143,8894,107,8868,485,202,113,154,8874,8886,138,537],[141,46,182,8920,104,349,8904,44,198,536,375,8887,79,8841,403,513,588,488,77,8899,579,96,530,96,334,112,120,433,480,192,477,470,79,153,147],[364,8903,144,496,582,330,177,8867,352,337,213,607,457,435,502,429,83,538,8898,492,502,200,479,8890,560,549,169,326,348,4846,143,114,211,8916,545],[465,8902,157,106,350,127,144,480,406,480,474,588,606,448,84,8918,506,8921,419,373,8881,53,89,420,8850,140,487,335,75,128,181,346,145,331,8872],[130,8913,8859,88,477,80,357,553,122,212,8910,607,586,336,99,469,560,159,340,80,8912,8910,338,209,89,340,8886,46,578,8921,116,518,8910,386,520],[492,498,534,381,113,139,387,419,177,525,8885,76,482,370,101,118,544,606,350,8851,418,514,481,179,565,147,216,135,347,460,569,604,189,8886,578],[421,473,493,146,101,108,430,97,115,510,159,335,8851,51,8900,488,200,8845,332,561,467,467,507,79,201,101,575,460,544,342,361,450,129,583,514],[208,193,185,467,172,545,8851,541,201,188,8896,155,544,419,82,539,459,550,141,508,8899,478,350,8904,8851,438,203,420,46,106,153,463,8904,572,406],[438,631,497,41,429,185,542,531,8859,120,208,8883,424,118,532,91,133,176,138,438,124,208,161,84,8904,106,65,104,8919,480,164,64,201,327,357],[8909,326,537,8907,541,181,8921,214,8894,371,478,487,8915,161,575,426,133,167,327,8872,568,115,98,8882,172,327,8877,214,8860,8902,8921,8855,195,361,82],[104,216,534,107,137,607,342,557,8913,171,542,8863,79,8879,176,374,203,8910,498,476,492,8873,495,513,119,559,500,347,374,444,216,8872,575,8869,39],[8849,608,123,189,546,196,454,8886,8865,344,8911,468,79,539,8850,8861,184,183,375,8872,167,451,421,199,8858,557,8900,469,210,128,551,607,55,8869,573],[90,8886,564,475,484,326,8903,586,159,175,146,430,493,44,8890,8909,419,607,348,380,182,369,8898,8923,343,116,8912,204,402,477,564,120,38,8924,190],[112,151,475,336,571,49,98,134,487,8906,8843,209,501,605,152,8845,73,428,84,105,8864,191,8872,200,175,8876,576,8869,8856,207,44,133,477,435,140],[565,572,533,518,74,515,512,145,529,337,553,209,8917,164,216,344,587,582,348,8901,457,8859,490,542,8896,112,168,403,344,8879,210,194,114,8919,441],[550,177,510,497,70,8921,8846,8901,8913,133,508,54,90,380,493,371,432,531,8908,8892,406,353,8841,502,8862,440,515,68,510,8883,402,158,41,128,508],[8919,380,463,139,496,8894,67,504,341,164,8882,111,125,535,8906,8871,176,121,56,467,91,487,8861,572,344,8866,498,8914,483,203,581,326,201,153,461],[605,8904,507,126,129,449,8913,370,341,128,8922,207,8851,169,8874,8841,177,152,8875,490,495,448,57,160,70,341,197,75,540,347,190,574,531,568,431],[458,435,41,141,407,346,510,100,207,164,124,204,583,501,130,490,579,129,534,509,207,568,477,8872,8906,479,8907,172,504,360,8851,8858,99,54,8852],[50,8860,454,106,532,177,48,363,64,327,106,175,8892,4846,214,100,550,8850,46,363,8923,208,111,116,327,122,106,174,127,495,533,142,162,188,456],[201,8918,8924,407,8865,53,369,109,98,369,343,558,501,160,525,524,47,131,8909,129,353,523,580,459,8910,448,529,8878,580,148,524,8848,519,516,607],[178,375,573,365,555,538,8917,103,157,174,420,8910,8884,377,125,475,8888,211,8893,100,58,144,193,8844,478,474,158,577,428,43,89,211,507,498,64],[124,336,339,509,8912,329,160,102,79,331,8861,533,464,132,123,82,8858,110,487,560,216,85,631,351,8887,476,541,180,370,534,523,402,450,169,363],[8851,205,344,491,8847,430,47,8921,8860,354,147,212,351,70,510,504,326,38,501,333,142,189,117,383,531,54,104,8863,194,182,8898,458,139,431,191],[197,203,328,526,190,8871,538,38,52,377,461,535,443,47,8881,365,506,103,545,208,191,435,174,47,530,608,8885,172,326,181,379,357,552,556,38],[42,159,534,200,365,8859,338,102,337,156,482,329,109,64,122,511,562,213,98,493,448,8864,326,148,8866,8853,377,484,559,585,606,549,164,324,8878],[139,186,334,8844,383,337,8851,57,174,100,454,104,151,540,387,122,482,8857,138,196,606,87,48,72,370,216,605,206,8841,551,8885,46,379,55,558],[207,196,206,50,500,584,574,210,468,58,174,536,460,214,509,8867,207,581,462,8863,8857,60,8901,127,8872,566,134,485,516,462,498,520,423,447,75],[585,8866,132,55,566,88,333,57,463,585,74,470,46,8853,8850,534,8871,8877,530,484,333,135,585,8859,436,333,431,523,470,211,8846,8893,481,8857,82],[373,91,493,363,454,169,157,430,342,464,155,537,144,8907,8907,8878,363,8905,451,506,496,335,8847,142,8913,513,124,494,166,139,349,544,170,608,134],[549,84,443,370,54,507,335,8886,8851,387,560,443,425,475,519,142,132,456,191,8879,8877,44,441,50,98,208,422,8864,8880,8850,89,559,538,608,8881],[196,110,8892,8922,156,174,344,517,365,462,105,8850,560,473,38,361,110,212,187,8898,458,193,498,183,114,72,406,541,103,555,338,158,8860,212,197],[544,8911,480,361,579,8892,8888,166,565,582,544,8855,525,138,576,8880,529,182,166,8861,8856,456,8895,424,438,135,8908,373,436,8894,173,168,8884,179,8841],[327,165,327,170,54,582,8906,160,429,565,112,328,147,8922,364,126,375,606,431,538,39,8922,537,460,8875,460,8893,580,85,76,52,41,460,8924,539],[605,179,480,129,540,8845,511,8860,444,8894,532,326,106,572,207,587,8853,8916,8899,8860,558,8924,546,8862,8859,546,8891,461,494,118,157,502,8864,8895,352],[478,499,367,141,332,173,331,8905,509,54,456,79,354,330,67,117,509,185,348,189,8902,443,204,469,387,556,196,182,134,67,8869,185,94,8856,8912],[8892,108,8924,51,8853,514,175,182,123,485,8893,449,159,160,208,8889,458,345,343,8898,551,457,418,542,8861,352,146,588,128,454,501,8863,117,148,8917],[511,331,553,216,8914,334,137,171,542,181,8863,534,8914,150,8921,192,82,490,539,187,206,535,143,118,213,100,425,406,560,170,94,494,75,198,576],[403,607,39,363,360,8873,348,8905,508,8858,148,103,584,8905,339,465,327,357,8895,488,97,581,199,73,512,572,478,93,8855,422,8860,544,8871,88,198],[425,52,115,326,152,8857,478,535,580,579,8918,8905,544,8898,538,8873,171,436,189,142,339,427,142,87,605,511,436,41,131,544,608,129,114,494,208],[179,178,8918,360,561,104,8875,377,8918,151,457,185,539,137,462,121,199,51,144,8905,8886,8899,567,495,180,8912,8896,77,206,8860,488,165,159,90,546],[194,137,341,170,157,112,8874,8919,550,168,8890,4846,52,8900,324,337,8862,336,171,8893,631,115,158,204,449,470,8881,114,72,345,8890,108,496,8903,8891],[422,149,213,487,500,94,515,587,8847,469,198,8900,8865,476,533,65,189,200,546,512,459,387,566,147,576,8887,92,82,207,8920,121,8843,436,562,558],[580,109,422,490,180,124,126,403,420,8879,513,192,429,8859,436,123,56,8858,471,216,127,8883,481,490,438,352,8891,560,111,8920,588,8905,171,214,8881],[8906,485,8911,210,421,73,470,8863,8897,493,369,113,8875,512,8876,100,8906,171,587,126,331,148,4846,8901,55,101,8863,8860,484,123,8879,8849,8847,56,113],[367,482,60,70,189,164,580,155,479,129,115,335,538,148,423,8856,8884,67,95,114,509,115,8895,525,504,8884,574,85,8910,195,187,508,606,529,143],[4846,575,8852,202,346,329,191,151,429,8909,8873,494,518,607,346,327,147,443,490,538,428,351,201,463,8890,8853,67,8847,449,480,530,492,381,159,360],[8881,327,65,567,135,8912,562,103,485,111,202,93,8891,403,500,509,103,74,507,365,8855,509,383,206,177,206,8880,456,387,8847,185,8897,506,561,51],[418,538,130,508,125,149,504,511,433,504,375,550,8872,67,8866,564,8859,124,8917,146,431,8880,8920,72,38,8843,537,118,375,119,190,608,343,377,441],[8872,8864,197,344,111,568,525,324,497,204,210,139,508,340,211,518,103,80,96,573,432,8855,104,576,607,8842,553,369,128,101,490,84,92,511,144],[8879,213,572,182,340,339,108,8909,8887,8844,488,116,498,607,369,497,164,127,422,8901,134,538,558,444,508,433,132,438,158,457,8924,8891,182,121,419],[53,8918,76,477,538,137,8892,455,127,481,8858,181,126,380,431,336,198,8906,80,582,174,79,528,125,533,506,536,538,604,138,8885,146,153,72,187],[207,347,206,8915,192,435,607,559,565,8845,141,150,571,42,171,49,8895,190,425,8844,102,504,197,473,169,144,536,8880,534,430,381,324,167,578,553],[605,73,8885,388,179,8875,8868,330,116,494,8881,529,526,580,565,8908,110,8883,586,519,162,470,164,8849,8873,514,54,558,331,131,8857,8870,559,8890,583],[455,8913,336,540,354,8852,216,511,8852,327,561,481,324,8867,566,186,453,8886,509,8891,120,8843,386,8922,479,526,8850,209,8918,8917,568,73,448,177,463],[8870,8909,166,365,470,178,209,557,175,586,337,354,436,173,169,429,574,125,324,8860,605,8894,65,50,555,482,111,481,377,558,550,8863,176,491,8911],[199,576,46,510,8844,557,117,557,388,561,167,8886,539,115,514,8907,181,8857,51,345,8896,157,563,171,447,8902,122,48,568,8923,496,147,448,8863,8872],[374,59,8921,8863,143,367,545,125,377,8867,534,377,67,583,8848,121,440,454,199,134,357,343,519,436,342,8878,148,329,154,8921,475,8857,192,204,8874],[140,143,346,121,8844,8913,178,68,8871,94,172,145,170,8921,541,488,331,582,44,578,161,427,407,354,8905,8852,108,8864,431,330,203,108,108,206,125],[8872,194,580,329,58,155,403,363,438,8903,8885,488,177,93,56,8879,348,586,190,428,452,335,440,8860,533,357,326,8906,166,557,518,500,8864,8918,465],[8906,112,214,8882,8881,544,485,357,379,377,68,8852,488,165,558,453,8863,55,8919,128,337,143,574,334,403,102,8881,8876,8854,8888,425,8845,74,589,87],[480,177,59,370,361,360,334,460,447,344,172,537,498,8858,119,145,198,461,159,433,182,8923,154,485,577,343,8841,434,431,159,585,8870,588,518,131],[146,8869,90,150,76,8910,508,514,110,8919,8905,344,328,327,419,108,187,379,82,80,8898,122,107,565,331,214,574,351,345,47,8910,135,8848,55,179],[50,443,195,573,431,422,477,463,568,473,8858,130,526,473,577,8922,58,541,438,8911,94,353,497,210,451,535,498,8900,453,189,158,214,8896,569,419],[189,40,140,8887,216,8856,560,8906,471,213,538,74,192,189,8877,433,379,99,191,8874,498,8879,201,552,114,42,430,450,131,544,501,8884,70,89,131],[433,556,8843,482,490,440,496,559,94,575,183,213,175,558,135,196,530,492,453,8866,8870,418,65,193,559,8913,146,164,72,8916,339,330,204,422,8868],[101,8872,449,471,326,199,116,47,357,336,8856,114,517,549,8842,422,463,546,443,426,97,8852,549,449,337,109,188,371,491,338,428,562,458,531,142],[4846,8897,336,165,68,73,148,510,8918,432,375,436,345,430,567,608,8862,87,460,8897,8869,86,8906,357,8867,182,357,140,8841,193,8853,8859,91,53,209],[463,96,468,8854,326,380,604,208,403,572,604,402,631,331,176,8912,533,518,512,377,524,68,336,339,487,440,8887,406,447,158,552,8850,537,98,76],[203,152,60,8911,47,367,514,79,357,122,154,452,8857,535,8899,144,8887,184,146,463,173,205,65,47,166,607,8895,607,116,585,476,65,135,149,8912],[160,42,589,513,190,523,8866,456,425,125,157,350,8871,490,529,143,56,8867,158,565,129,52,449,511,419,493,584,163,122,367,101,369,326,520,374],[43,168,160,428,8887,516,329,160,8867,581,502,192,105,82,351,205,575,8921,72,8875,583,436,513,8850,200,608,440,338,379,8888,8855,8854,436,181,4846],[8903,580,508,455,47,8880,8876,171,132,480,340,419,576,142,571,331,8885,357,213,8855,353,8915,542,519,363,8896,213,184,8874,433,135,386,52,74,180],[332,371,8918,56,8904,553,419,8885,586,468,157,103,605,172,96,538,562,88,106,8902,546,349,158,8887,531,89,566,8851,44,210,126,8918,8883,127,431],[8876,8906,204,46,125,361,546,70,538,93,138,349,8900,568,8848,140,210,8845,8857,402,8879,425,534,8904,589,8903,110,8912,8902,421,197,64,89,386,426]]')]
#     insert_recommended_list(session, recs, 100)