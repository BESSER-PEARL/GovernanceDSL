# Generated from govdsl.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,59,650,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,
        13,7,13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,
        19,2,20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,
        26,7,26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,
        32,2,33,7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,
        39,7,39,2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,
        45,2,46,7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,2,
        52,7,52,2,53,7,53,2,54,7,54,2,55,7,55,2,56,7,56,2,57,7,57,2,58,7,
        58,1,0,1,0,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,
        3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,
        4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,
        5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,
        6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,
        7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,
        7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,
        9,1,9,1,9,1,9,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,
        1,12,1,12,1,12,1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,14,
        1,14,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,16,1,16,1,16,
        1,16,1,16,1,17,1,17,1,17,1,17,1,17,1,17,1,18,1,18,1,18,1,18,1,18,
        1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,19,1,19,1,19,1,19,1,20,
        1,20,1,20,1,20,1,20,1,20,1,20,1,21,1,21,1,21,1,21,1,21,1,21,1,21,
        1,21,1,21,1,21,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,23,
        1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,24,1,24,1,24,1,24,1,24,1,24,
        1,24,1,25,1,25,1,25,1,25,1,25,1,25,1,26,1,26,1,26,1,26,1,26,1,26,
        1,26,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,28,1,28,1,28,1,28,
        1,28,1,28,1,28,1,29,1,29,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,
        1,30,1,30,1,30,1,30,1,30,1,31,1,31,1,31,1,31,1,31,1,31,1,32,1,32,
        1,32,1,32,1,32,1,32,1,32,1,32,1,32,1,32,1,32,1,32,1,33,1,33,1,33,
        1,34,1,34,1,34,1,34,1,34,1,34,1,34,1,34,1,34,1,34,1,34,1,34,1,34,
        1,34,1,34,1,34,1,35,1,35,1,35,1,35,1,35,1,35,1,35,1,35,1,35,1,35,
        1,35,1,36,1,36,1,36,1,36,1,36,1,36,1,36,1,36,1,36,1,37,1,37,1,37,
        1,37,1,37,1,38,1,38,1,38,1,38,1,38,1,38,1,39,1,39,1,39,1,39,1,39,
        1,39,1,39,1,40,1,40,1,40,1,40,1,40,1,40,1,41,1,41,1,41,1,41,1,41,
        1,41,1,41,1,41,1,41,1,41,1,41,1,41,1,41,1,41,1,41,1,41,1,41,1,41,
        1,41,1,41,1,41,1,42,1,42,1,42,1,42,1,42,1,42,1,42,1,42,1,42,1,42,
        1,42,1,42,1,42,1,42,1,42,1,42,1,43,1,43,1,43,1,43,1,43,1,43,1,43,
        1,43,1,43,1,43,1,43,1,44,1,44,1,44,1,44,1,44,1,44,1,45,1,45,1,45,
        1,45,1,45,1,45,1,45,1,45,1,46,1,46,1,46,1,46,1,46,1,46,1,47,1,47,
        1,47,1,47,1,47,1,47,1,47,1,47,1,47,1,47,1,48,1,48,1,48,1,48,1,48,
        1,48,1,48,1,48,1,48,1,48,1,48,1,49,1,49,1,49,1,49,1,49,1,49,1,49,
        1,49,1,49,1,50,1,50,1,50,1,50,1,50,1,50,1,50,1,50,1,50,1,50,1,50,
        1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,52,1,52,1,52,
        1,52,1,52,1,53,1,53,1,53,1,53,1,53,1,53,1,54,1,54,1,54,1,54,1,54,
        1,54,1,54,1,55,1,55,5,55,616,8,55,10,55,12,55,619,9,55,1,56,3,56,
        622,8,56,1,56,4,56,625,8,56,11,56,12,56,626,1,57,4,57,630,8,57,11,
        57,12,57,631,1,57,1,57,4,57,636,8,57,11,57,12,57,637,1,58,1,58,3,
        58,642,8,58,1,58,4,58,645,8,58,11,58,12,58,646,1,58,1,58,0,0,59,
        1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,12,25,13,
        27,14,29,15,31,16,33,17,35,18,37,19,39,20,41,21,43,22,45,23,47,24,
        49,25,51,26,53,27,55,28,57,29,59,30,61,31,63,32,65,33,67,34,69,35,
        71,36,73,37,75,38,77,39,79,40,81,41,83,42,85,43,87,44,89,45,91,46,
        93,47,95,48,97,49,99,50,101,51,103,52,105,53,107,54,109,55,111,56,
        113,57,115,58,117,59,1,0,4,3,0,65,90,95,95,97,122,4,0,48,57,65,90,
        95,95,97,122,1,0,48,57,2,0,9,9,32,32,657,0,1,1,0,0,0,0,3,1,0,0,0,
        0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,
        15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,
        25,1,0,0,0,0,27,1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,0,33,1,0,0,0,0,
        35,1,0,0,0,0,37,1,0,0,0,0,39,1,0,0,0,0,41,1,0,0,0,0,43,1,0,0,0,0,
        45,1,0,0,0,0,47,1,0,0,0,0,49,1,0,0,0,0,51,1,0,0,0,0,53,1,0,0,0,0,
        55,1,0,0,0,0,57,1,0,0,0,0,59,1,0,0,0,0,61,1,0,0,0,0,63,1,0,0,0,0,
        65,1,0,0,0,0,67,1,0,0,0,0,69,1,0,0,0,0,71,1,0,0,0,0,73,1,0,0,0,0,
        75,1,0,0,0,0,77,1,0,0,0,0,79,1,0,0,0,0,81,1,0,0,0,0,83,1,0,0,0,0,
        85,1,0,0,0,0,87,1,0,0,0,0,89,1,0,0,0,0,91,1,0,0,0,0,93,1,0,0,0,0,
        95,1,0,0,0,0,97,1,0,0,0,0,99,1,0,0,0,0,101,1,0,0,0,0,103,1,0,0,0,
        0,105,1,0,0,0,0,107,1,0,0,0,0,109,1,0,0,0,0,111,1,0,0,0,0,113,1,
        0,0,0,0,115,1,0,0,0,0,117,1,0,0,0,1,119,1,0,0,0,3,121,1,0,0,0,5,
        123,1,0,0,0,7,138,1,0,0,0,9,153,1,0,0,0,11,172,1,0,0,0,13,195,1,
        0,0,0,15,211,1,0,0,0,17,231,1,0,0,0,19,244,1,0,0,0,21,250,1,0,0,
        0,23,252,1,0,0,0,25,260,1,0,0,0,27,265,1,0,0,0,29,272,1,0,0,0,31,
        274,1,0,0,0,33,283,1,0,0,0,35,288,1,0,0,0,37,294,1,0,0,0,39,307,
        1,0,0,0,41,311,1,0,0,0,43,318,1,0,0,0,45,328,1,0,0,0,47,337,1,0,
        0,0,49,345,1,0,0,0,51,352,1,0,0,0,53,358,1,0,0,0,55,365,1,0,0,0,
        57,373,1,0,0,0,59,380,1,0,0,0,61,382,1,0,0,0,63,395,1,0,0,0,65,401,
        1,0,0,0,67,413,1,0,0,0,69,416,1,0,0,0,71,432,1,0,0,0,73,443,1,0,
        0,0,75,452,1,0,0,0,77,457,1,0,0,0,79,463,1,0,0,0,81,470,1,0,0,0,
        83,476,1,0,0,0,85,497,1,0,0,0,87,513,1,0,0,0,89,524,1,0,0,0,91,530,
        1,0,0,0,93,538,1,0,0,0,95,544,1,0,0,0,97,554,1,0,0,0,99,565,1,0,
        0,0,101,574,1,0,0,0,103,585,1,0,0,0,105,595,1,0,0,0,107,600,1,0,
        0,0,109,606,1,0,0,0,111,613,1,0,0,0,113,621,1,0,0,0,115,629,1,0,
        0,0,117,644,1,0,0,0,119,120,5,123,0,0,120,2,1,0,0,0,121,122,5,125,
        0,0,122,4,1,0,0,0,123,124,5,67,0,0,124,125,5,111,0,0,125,126,5,109,
        0,0,126,127,5,112,0,0,127,128,5,111,0,0,128,129,5,115,0,0,129,130,
        5,101,0,0,130,131,5,100,0,0,131,132,5,80,0,0,132,133,5,111,0,0,133,
        134,5,108,0,0,134,135,5,105,0,0,135,136,5,99,0,0,136,137,5,121,0,
        0,137,6,1,0,0,0,138,139,5,77,0,0,139,140,5,97,0,0,140,141,5,106,
        0,0,141,142,5,111,0,0,142,143,5,114,0,0,143,144,5,105,0,0,144,145,
        5,116,0,0,145,146,5,121,0,0,146,147,5,80,0,0,147,148,5,111,0,0,148,
        149,5,108,0,0,149,150,5,105,0,0,150,151,5,99,0,0,151,152,5,121,0,
        0,152,8,1,0,0,0,153,154,5,76,0,0,154,155,5,101,0,0,155,156,5,97,
        0,0,156,157,5,100,0,0,157,158,5,101,0,0,158,159,5,114,0,0,159,160,
        5,68,0,0,160,161,5,114,0,0,161,162,5,105,0,0,162,163,5,118,0,0,163,
        164,5,101,0,0,164,165,5,110,0,0,165,166,5,80,0,0,166,167,5,111,0,
        0,167,168,5,108,0,0,168,169,5,105,0,0,169,170,5,99,0,0,170,171,5,
        121,0,0,171,10,1,0,0,0,172,173,5,65,0,0,173,174,5,98,0,0,174,175,
        5,115,0,0,175,176,5,111,0,0,176,177,5,108,0,0,177,178,5,117,0,0,
        178,179,5,116,0,0,179,180,5,101,0,0,180,181,5,77,0,0,181,182,5,97,
        0,0,182,183,5,106,0,0,183,184,5,111,0,0,184,185,5,114,0,0,185,186,
        5,105,0,0,186,187,5,116,0,0,187,188,5,121,0,0,188,189,5,80,0,0,189,
        190,5,111,0,0,190,191,5,108,0,0,191,192,5,105,0,0,192,193,5,99,0,
        0,193,194,5,121,0,0,194,12,1,0,0,0,195,196,5,67,0,0,196,197,5,111,
        0,0,197,198,5,110,0,0,198,199,5,115,0,0,199,200,5,101,0,0,200,201,
        5,110,0,0,201,202,5,115,0,0,202,203,5,117,0,0,203,204,5,115,0,0,
        204,205,5,80,0,0,205,206,5,111,0,0,206,207,5,108,0,0,207,208,5,105,
        0,0,208,209,5,99,0,0,209,210,5,121,0,0,210,14,1,0,0,0,211,212,5,
        76,0,0,212,213,5,97,0,0,213,214,5,122,0,0,214,215,5,121,0,0,215,
        216,5,67,0,0,216,217,5,111,0,0,217,218,5,110,0,0,218,219,5,115,0,
        0,219,220,5,101,0,0,220,221,5,110,0,0,221,222,5,115,0,0,222,223,
        5,117,0,0,223,224,5,115,0,0,224,225,5,80,0,0,225,226,5,111,0,0,226,
        227,5,108,0,0,227,228,5,105,0,0,228,229,5,99,0,0,229,230,5,121,0,
        0,230,16,1,0,0,0,231,232,5,86,0,0,232,233,5,111,0,0,233,234,5,116,
        0,0,234,235,5,105,0,0,235,236,5,110,0,0,236,237,5,103,0,0,237,238,
        5,80,0,0,238,239,5,111,0,0,239,240,5,108,0,0,240,241,5,105,0,0,241,
        242,5,99,0,0,242,243,5,121,0,0,243,18,1,0,0,0,244,245,5,83,0,0,245,
        246,5,99,0,0,246,247,5,111,0,0,247,248,5,112,0,0,248,249,5,101,0,
        0,249,20,1,0,0,0,250,251,5,58,0,0,251,22,1,0,0,0,252,253,5,80,0,
        0,253,254,5,114,0,0,254,255,5,111,0,0,255,256,5,106,0,0,256,257,
        5,101,0,0,257,258,5,99,0,0,258,259,5,116,0,0,259,24,1,0,0,0,260,
        261,5,102,0,0,261,262,5,114,0,0,262,263,5,111,0,0,263,264,5,109,
        0,0,264,26,1,0,0,0,265,266,5,71,0,0,266,267,5,105,0,0,267,268,5,
        116,0,0,268,269,5,72,0,0,269,270,5,117,0,0,270,271,5,98,0,0,271,
        28,1,0,0,0,272,273,5,47,0,0,273,30,1,0,0,0,274,275,5,65,0,0,275,
        276,5,99,0,0,276,277,5,116,0,0,277,278,5,105,0,0,278,279,5,118,0,
        0,279,280,5,105,0,0,280,281,5,116,0,0,281,282,5,121,0,0,282,32,1,
        0,0,0,283,284,5,84,0,0,284,285,5,97,0,0,285,286,5,115,0,0,286,287,
        5,107,0,0,287,34,1,0,0,0,288,289,5,73,0,0,289,290,5,115,0,0,290,
        291,5,115,0,0,291,292,5,117,0,0,292,293,5,101,0,0,293,36,1,0,0,0,
        294,295,5,80,0,0,295,296,5,117,0,0,296,297,5,108,0,0,297,298,5,108,
        0,0,298,299,5,32,0,0,299,300,5,114,0,0,300,301,5,101,0,0,301,302,
        5,113,0,0,302,303,5,117,0,0,303,304,5,101,0,0,304,305,5,115,0,0,
        305,306,5,116,0,0,306,38,1,0,0,0,307,308,5,65,0,0,308,309,5,108,
        0,0,309,310,5,108,0,0,310,40,1,0,0,0,311,312,5,83,0,0,312,313,5,
        116,0,0,313,314,5,97,0,0,314,315,5,116,0,0,315,316,5,117,0,0,316,
        317,5,115,0,0,317,42,1,0,0,0,318,319,5,99,0,0,319,320,5,111,0,0,
        320,321,5,109,0,0,321,322,5,112,0,0,322,323,5,108,0,0,323,324,5,
        101,0,0,324,325,5,116,0,0,325,326,5,101,0,0,326,327,5,100,0,0,327,
        44,1,0,0,0,328,329,5,97,0,0,329,330,5,99,0,0,330,331,5,99,0,0,331,
        332,5,101,0,0,332,333,5,112,0,0,333,334,5,116,0,0,334,335,5,101,
        0,0,335,336,5,100,0,0,336,46,1,0,0,0,337,338,5,112,0,0,338,339,5,
        97,0,0,339,340,5,114,0,0,340,341,5,116,0,0,341,342,5,105,0,0,342,
        343,5,97,0,0,343,344,5,108,0,0,344,48,1,0,0,0,345,346,5,65,0,0,346,
        347,5,99,0,0,347,348,5,116,0,0,348,349,5,105,0,0,349,350,5,111,0,
        0,350,351,5,110,0,0,351,50,1,0,0,0,352,353,5,109,0,0,353,354,5,101,
        0,0,354,355,5,114,0,0,355,356,5,103,0,0,356,357,5,101,0,0,357,52,
        1,0,0,0,358,359,5,114,0,0,359,360,5,101,0,0,360,361,5,118,0,0,361,
        362,5,105,0,0,362,363,5,101,0,0,363,364,5,119,0,0,364,54,1,0,0,0,
        365,366,5,114,0,0,366,367,5,101,0,0,367,368,5,108,0,0,368,369,5,
        101,0,0,369,370,5,97,0,0,370,371,5,115,0,0,371,372,5,101,0,0,372,
        56,1,0,0,0,373,374,5,76,0,0,374,375,5,97,0,0,375,376,5,98,0,0,376,
        377,5,101,0,0,377,378,5,108,0,0,378,379,5,115,0,0,379,58,1,0,0,0,
        380,381,5,44,0,0,381,60,1,0,0,0,382,383,5,80,0,0,383,384,5,97,0,
        0,384,385,5,114,0,0,385,386,5,116,0,0,386,387,5,105,0,0,387,388,
        5,99,0,0,388,389,5,105,0,0,389,390,5,112,0,0,390,391,5,97,0,0,391,
        392,5,110,0,0,392,393,5,116,0,0,393,394,5,115,0,0,394,62,1,0,0,0,
        395,396,5,82,0,0,396,397,5,111,0,0,397,398,5,108,0,0,398,399,5,101,
        0,0,399,400,5,115,0,0,400,64,1,0,0,0,401,402,5,73,0,0,402,403,5,
        110,0,0,403,404,5,100,0,0,404,405,5,105,0,0,405,406,5,118,0,0,406,
        407,5,105,0,0,407,408,5,100,0,0,408,409,5,117,0,0,409,410,5,97,0,
        0,410,411,5,108,0,0,411,412,5,115,0,0,412,66,1,0,0,0,413,414,5,97,
        0,0,414,415,5,115,0,0,415,68,1,0,0,0,416,417,5,119,0,0,417,418,5,
        105,0,0,418,419,5,116,0,0,419,420,5,104,0,0,420,421,5,32,0,0,421,
        422,5,99,0,0,422,423,5,111,0,0,423,424,5,110,0,0,424,425,5,102,0,
        0,425,426,5,105,0,0,426,427,5,100,0,0,427,428,5,101,0,0,428,429,
        5,110,0,0,429,430,5,99,0,0,430,431,5,101,0,0,431,70,1,0,0,0,432,
        433,5,67,0,0,433,434,5,111,0,0,434,435,5,110,0,0,435,436,5,100,0,
        0,436,437,5,105,0,0,437,438,5,116,0,0,438,439,5,105,0,0,439,440,
        5,111,0,0,440,441,5,110,0,0,441,442,5,115,0,0,442,72,1,0,0,0,443,
        444,5,68,0,0,444,445,5,101,0,0,445,446,5,97,0,0,446,447,5,100,0,
        0,447,448,5,108,0,0,448,449,5,105,0,0,449,450,5,110,0,0,450,451,
        5,101,0,0,451,74,1,0,0,0,452,453,5,100,0,0,453,454,5,97,0,0,454,
        455,5,121,0,0,455,456,5,115,0,0,456,76,1,0,0,0,457,458,5,119,0,0,
        458,459,5,101,0,0,459,460,5,101,0,0,460,461,5,107,0,0,461,462,5,
        115,0,0,462,78,1,0,0,0,463,464,5,109,0,0,464,465,5,111,0,0,465,466,
        5,110,0,0,466,467,5,116,0,0,467,468,5,104,0,0,468,469,5,115,0,0,
        469,80,1,0,0,0,470,471,5,121,0,0,471,472,5,101,0,0,472,473,5,97,
        0,0,473,474,5,114,0,0,474,475,5,115,0,0,475,82,1,0,0,0,476,477,5,
        80,0,0,477,478,5,97,0,0,478,479,5,114,0,0,479,480,5,116,0,0,480,
        481,5,105,0,0,481,482,5,99,0,0,482,483,5,105,0,0,483,484,5,112,0,
        0,484,485,5,97,0,0,485,486,5,110,0,0,486,487,5,116,0,0,487,488,5,
        69,0,0,488,489,5,120,0,0,489,490,5,99,0,0,490,491,5,108,0,0,491,
        492,5,117,0,0,492,493,5,115,0,0,493,494,5,105,0,0,494,495,5,111,
        0,0,495,496,5,110,0,0,496,84,1,0,0,0,497,498,5,77,0,0,498,499,5,
        105,0,0,499,500,5,110,0,0,500,501,5,80,0,0,501,502,5,97,0,0,502,
        503,5,114,0,0,503,504,5,116,0,0,504,505,5,105,0,0,505,506,5,99,0,
        0,506,507,5,105,0,0,507,508,5,112,0,0,508,509,5,97,0,0,509,510,5,
        110,0,0,510,511,5,116,0,0,511,512,5,115,0,0,512,86,1,0,0,0,513,514,
        5,80,0,0,514,515,5,97,0,0,515,516,5,114,0,0,516,517,5,97,0,0,517,
        518,5,109,0,0,518,519,5,101,0,0,519,520,5,116,0,0,520,521,5,101,
        0,0,521,522,5,114,0,0,522,523,5,115,0,0,523,88,1,0,0,0,524,525,5,
        114,0,0,525,526,5,97,0,0,526,527,5,116,0,0,527,528,5,105,0,0,528,
        529,5,111,0,0,529,90,1,0,0,0,530,531,5,100,0,0,531,532,5,101,0,0,
        532,533,5,102,0,0,533,534,5,97,0,0,534,535,5,117,0,0,535,536,5,108,
        0,0,536,537,5,116,0,0,537,92,1,0,0,0,538,539,5,79,0,0,539,540,5,
        114,0,0,540,541,5,100,0,0,541,542,5,101,0,0,542,543,5,114,0,0,543,
        94,1,0,0,0,544,545,5,69,0,0,545,546,5,120,0,0,546,547,5,101,0,0,
        547,548,5,99,0,0,548,549,5,117,0,0,549,550,5,116,0,0,550,551,5,105,
        0,0,551,552,5,111,0,0,552,553,5,110,0,0,553,96,1,0,0,0,554,555,5,
        115,0,0,555,556,5,101,0,0,556,557,5,113,0,0,557,558,5,117,0,0,558,
        559,5,101,0,0,559,560,5,110,0,0,560,561,5,116,0,0,561,562,5,105,
        0,0,562,563,5,97,0,0,563,564,5,108,0,0,564,98,1,0,0,0,565,566,5,
        112,0,0,566,567,5,97,0,0,567,568,5,114,0,0,568,569,5,97,0,0,569,
        570,5,108,0,0,570,571,5,108,0,0,571,572,5,101,0,0,572,573,5,108,
        0,0,573,100,1,0,0,0,574,575,5,82,0,0,575,576,5,101,0,0,576,577,5,
        113,0,0,577,578,5,117,0,0,578,579,5,105,0,0,579,580,5,114,0,0,580,
        581,5,101,0,0,581,582,5,65,0,0,582,583,5,108,0,0,583,584,5,108,0,
        0,584,102,1,0,0,0,585,586,5,67,0,0,586,587,5,97,0,0,587,588,5,114,
        0,0,588,589,5,114,0,0,589,590,5,121,0,0,590,591,5,79,0,0,591,592,
        5,118,0,0,592,593,5,101,0,0,593,594,5,114,0,0,594,104,1,0,0,0,595,
        596,5,116,0,0,596,597,5,114,0,0,597,598,5,117,0,0,598,599,5,101,
        0,0,599,106,1,0,0,0,600,601,5,102,0,0,601,602,5,97,0,0,602,603,5,
        108,0,0,603,604,5,115,0,0,604,605,5,101,0,0,605,108,1,0,0,0,606,
        607,5,80,0,0,607,608,5,104,0,0,608,609,5,97,0,0,609,610,5,115,0,
        0,610,611,5,101,0,0,611,612,5,115,0,0,612,110,1,0,0,0,613,617,7,
        0,0,0,614,616,7,1,0,0,615,614,1,0,0,0,616,619,1,0,0,0,617,615,1,
        0,0,0,617,618,1,0,0,0,618,112,1,0,0,0,619,617,1,0,0,0,620,622,5,
        45,0,0,621,620,1,0,0,0,621,622,1,0,0,0,622,624,1,0,0,0,623,625,7,
        2,0,0,624,623,1,0,0,0,625,626,1,0,0,0,626,624,1,0,0,0,626,627,1,
        0,0,0,627,114,1,0,0,0,628,630,7,2,0,0,629,628,1,0,0,0,630,631,1,
        0,0,0,631,629,1,0,0,0,631,632,1,0,0,0,632,633,1,0,0,0,633,635,5,
        46,0,0,634,636,7,2,0,0,635,634,1,0,0,0,636,637,1,0,0,0,637,635,1,
        0,0,0,637,638,1,0,0,0,638,116,1,0,0,0,639,645,7,3,0,0,640,642,5,
        13,0,0,641,640,1,0,0,0,641,642,1,0,0,0,642,643,1,0,0,0,643,645,5,
        10,0,0,644,639,1,0,0,0,644,641,1,0,0,0,645,646,1,0,0,0,646,644,1,
        0,0,0,646,647,1,0,0,0,647,648,1,0,0,0,648,649,6,58,0,0,649,118,1,
        0,0,0,9,0,617,621,626,631,637,641,644,646,1,6,0,0
    ]

class govdslLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    T__15 = 16
    T__16 = 17
    T__17 = 18
    T__18 = 19
    T__19 = 20
    T__20 = 21
    T__21 = 22
    T__22 = 23
    T__23 = 24
    T__24 = 25
    T__25 = 26
    T__26 = 27
    T__27 = 28
    T__28 = 29
    T__29 = 30
    T__30 = 31
    T__31 = 32
    T__32 = 33
    T__33 = 34
    T__34 = 35
    T__35 = 36
    T__36 = 37
    T__37 = 38
    T__38 = 39
    T__39 = 40
    T__40 = 41
    T__41 = 42
    T__42 = 43
    T__43 = 44
    T__44 = 45
    T__45 = 46
    T__46 = 47
    T__47 = 48
    T__48 = 49
    T__49 = 50
    T__50 = 51
    T__51 = 52
    T__52 = 53
    T__53 = 54
    T__54 = 55
    ID = 56
    SIGNED_INT = 57
    FLOAT = 58
    WS = 59

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'{'", "'}'", "'ComposedPolicy'", "'MajorityPolicy'", "'LeaderDrivenPolicy'", 
            "'AbsoluteMajorityPolicy'", "'ConsensusPolicy'", "'LazyConsensusPolicy'", 
            "'VotingPolicy'", "'Scope'", "':'", "'Project'", "'from'", "'GitHub'", 
            "'/'", "'Activity'", "'Task'", "'Issue'", "'Pull request'", 
            "'All'", "'Status'", "'completed'", "'accepted'", "'partial'", 
            "'Action'", "'merge'", "'review'", "'release'", "'Labels'", 
            "','", "'Participants'", "'Roles'", "'Individuals'", "'as'", 
            "'with confidence'", "'Conditions'", "'Deadline'", "'days'", 
            "'weeks'", "'months'", "'years'", "'ParticipantExclusion'", 
            "'MinParticipants'", "'Parameters'", "'ratio'", "'default'", 
            "'Order'", "'Execution'", "'sequential'", "'parallel'", "'RequireAll'", 
            "'CarryOver'", "'true'", "'false'", "'Phases'" ]

    symbolicNames = [ "<INVALID>",
            "ID", "SIGNED_INT", "FLOAT", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "T__18", "T__19", 
                  "T__20", "T__21", "T__22", "T__23", "T__24", "T__25", 
                  "T__26", "T__27", "T__28", "T__29", "T__30", "T__31", 
                  "T__32", "T__33", "T__34", "T__35", "T__36", "T__37", 
                  "T__38", "T__39", "T__40", "T__41", "T__42", "T__43", 
                  "T__44", "T__45", "T__46", "T__47", "T__48", "T__49", 
                  "T__50", "T__51", "T__52", "T__53", "T__54", "ID", "SIGNED_INT", 
                  "FLOAT", "WS" ]

    grammarFileName = "govdsl.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


