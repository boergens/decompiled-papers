"""Text printed on the source-data pages of Ströh et al. 2022, read by eye from the page images (2026-10-17) and
checked against tesseract OCR (work/check_sd_titles.py). Per file: list over PDF pages of
(page title, model-map title or None, title of the second projection image). The first projection image is titled
't=0min' on every page; the colour maps are titled 'data' (and 'model: R2adj=..., SEres=...' in Figure 1—source data 1)."""
T = {
    "fig1-data1": [
        ("Os, IAC20190122_B20190120_2", "0.9725", "0.019589", "t=1381.2667min"),
        ("Os, IAC20190125_B20190123_1", "0.94437", "0.022404", "t=1383.0333min"),
        ("Os, IAC20190511_B20190509", "0.94519", "0.022827", "t=1364.5min"),
        ("Os, IAC20191027_B20191025", "0.9338", "0.035457", "t=1380.2667min"),
        ("Os, IAC20191101_B20191030", "0.95419", "0.027895", "t=1360.9167min"),
        ("Os, IAC20191114_B20191112", "0.94471", "0.027416", "t=1360.6167min"),
        ("Os, IAC20200115_B20190113", "0.94728", "0.028251", "t=1349.8833min"),
        ("Os, IAC20200118_B20200116", "0.96708", "0.024258", "t=1343.05min"),
        ("Os, IAC20201113_B20201111", "0.95792", "0.021907", "t=1343.7167min"),
        ("Os, IAC20201115_B20201113", "0.97435", "0.018621", "t=1337.7167min"),
        ("Os, IAC20201202_B20201130", "0.95779", "0.020163", "t=1345.1167min"),
        ("Os, IAC20201204_B20201202", "0.93064", "0.030301", "t=1342.9333min"),
        ("Os, IAC20201206_B20201204", "0.92675", "0.028264", "t=1347.5667min"),
    ],
    "fig1-data2": [
        ("redOs, IAC20190324_B20190322_1", None, None, "t=1339.8833min"),
        ("redOs, IAC20190516_B20190514", None, None, "t=1364.7833min"),
        ("redOs, IAC20191213_B20191211", None, None, "t=1356.8833min"),
        ("redOs, IAC20191214_B20191212", None, None, "t=1348.95min"),
        ("redOs, IAC20200117_B20200115", None, None, "t=1343.7167min"),
        ("redOs, IAC20200123_B20200121", None, None, "t=1349.3833min"),
    ],
    "fig1-data3": [
        ("redOs+5.56%Formamide, IAC20191212_B20191210", None, None, "t=1350.7667min"),
        ("redOs+5.56%Formamide, IAC20191215_B20191213", None, None, "t=1348.7333min"),
        ("redOs+5.56%Formamide, IAC20191218_B20191216", None, None, "t=1347.9333min"),
        ("redOs+5.56%Formamide, IAC20191219_B20191217", None, None, "t=1351.2167min"),
    ],
    "fig1-data4": [
        ("redOs+11.25%Formamide, IAC20191029_B20191027", None, None, "t=1351min"),
        ("redOs+11.25%Formamide, IAC20191031_B20191029", None, None, "t=1354.5333min"),
        ("redOs+11.25%Formamide, IAC20191103_B20191101", None, None, "t=1355.5667min"),
        ("redOs+11.25%Formamide, IAC20191116_B20191114", None, None, "t=1355.2333min"),
    ],
    "fig1-data5": [
        ("FerriOs, IAC20211124_B20211122", None, None, "t=1347.6833min"),
        ("FerriOs, IAC20211202_B20211130", None, None, "t=1346.5667min"),
    ],
    "fig2-data1": [
        ("KFeCN, IAC20191028_B20191025", None, None, "t=1349.8667min"),
        ("KFeCN, IAC20191102_B20191030", None, None, "t=1298.5min"),
        ("KFeCN, IAC20191115_B20191112", None, None, "t=1354.6min"),
        ("KFeCN, IAC20200116_B20190113", None, None, "t=1350.05min"),
        ("KFeCN, IAC20200119_B20200116", None, None, "t=1350.7167min"),
        ("KFeCN, IAC20200122_B20200119", None, None, "t=1351.4167min"),
    ],
    "fig2-data2": [
        ("Ferri, IAC20220121_B20220118", None, None, "t=1344.95min"),
        ("Ferri, IAC20220123_B20220120", None, None, "t=1349.75min"),
        ("Ferri, IAC20220204_B20220201", None, None, "t=1345.3min"),
        ("Ferri, IAC20220211_B20220208", None, None, "t=1353.4333min"),
    ],
}
