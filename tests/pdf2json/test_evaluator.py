import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..."))
from evaluator import Validate
from metrics import SimilarityMetrics
from models import PageData, PageGenerate, PageSize, ParserData, Scores, TransformData


class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.gt_data = ParserData(
            pages={
                "1": PageData(
                    size=PageSize(top=0.0, left=0.0, height=1170.0, width=810.0),
                    data=[
                        '<text top="1136" left="619" width="160" height="18" font="0"><b>www.innodisk.com</b></text>\n',
                        '<text top="735" left="22" width="126" height="13" font="1"><b>Headquarters (Taiwan) </b></text>\n',
                        '<text top="751" left="22" width="154" height="13" font="2">5F., No.237, Sec. 1, Datong Rd., </text>\n',
                        '<text top="764" left="22" width="152" height="13" font="2">Xizhi Dist., New Taipei City 221, </text>\n',
                        '<text top="776" left="22" width="33" height="13" font="2">Taiwan</text>\n',
                        '<text top="789" left="22" width="113" height="13" font="2">Tel: +886-2-7703-3000 </text>\n',
                        '<text top="802" left="22" width="124" height="13" font="2">Email: sales@innodisk.com</text>\n',
                        '<text top="823" left="22" width="80" height="13" font="1"><b>Branch Offices:</b></text>\n',
                        '<text top="839" left="22" width="22" height="13" font="1"><b>USA</b></text>\n',
                        '<text top="851" left="32" width="108" height="13" font="3"><a href="mailto:usasales@innodisk.com">usasales@innodisk.com</a></text>\n',
                        '<text top="864" left="32" width="82" height="13" font="2">+1-510-770-9421</text>\n',
                        '<text top="876" left="22" width="37" height="13" font="1"><b>Europe</b></text>\n',
                        '<text top="889" left="32" width="104" height="13" font="3"><a href="mailto:eusales@innodisk.com">eusales@innodisk.com</a></text>\n',
                        '<text top="902" left="32" width="82" height="13" font="2">+31-40-3045-400</text>\n',
                        '<text top="914" left="22" width="31" height="13" font="1"><b>Japan</b></text>\n',
                        '<text top="927" left="32" width="101" height="13" font="3"><a href="mailto:jpsales@innodisk.com">jpsales@innodisk.com</a></text>\n',
                        '<text top="939" left="32" width="82" height="13" font="2">+81-45-594-7581</text>\n',
                        '<text top="952" left="22" width="30" height="13" font="1"><b>China</b></text>\n',
                        '<text top="965" left="32" width="109" height="13" font="3"><a href="mailto:sales_cn@innodisk.com">sales_cn@innodisk.com</a></text>\n',
                        '<text top="977" left="32" width="94" height="13" font="2">+86-755-2167-3689</text>\n',
                        '<text top="1005" left="22" width="101" height="13" font="4"><a href="http://www.innodisk.com/"><b>www.innodisk.com</b></a></text>\n',
                        '<text top="1021" left="22" width="143" height="13" font="2">©  2018 Innodisk Corporation. </text>\n',
                        '<text top="1034" left="22" width="151" height="13" font="2">All right reserved. Specifications </text>\n',
                        '<text top="1046" left="22" width="141" height="13" font="2">are subject to change without </text>\n',
                        '<text top="1059" left="22" width="56" height="13" font="2">prior notice.</text>\n',
                        '<text top="1084" left="22" width="66" height="9" font="5">November 24, 2022</text>\n',
                        '<text top="372" left="22" width="203" height="22" font="6"><b>Mechanical Drawing</b></text>\n',
                        '<text top="713" left="183" width="141" height="22" font="6"><b>Specifications</b></text>\n',
                        '<text top="108" left="405" width="88" height="22" font="6"><b>Features</b></text>\n',
                        '<text top="744" left="268" width="85" height="19" font="7">Form-Factor</text>\n',
                        '<text top="744" left="370" width="46" height="19" font="8">mPCIe</text>\n',
                        '<text top="771" left="291" width="62" height="19" font="7">Input I/F</text>\n',
                        '<text top="771" left="370" width="114" height="19" font="8">PCI Express 2.0 </text>\n',
                        '<text top="799" left="280" width="73" height="19" font="7">Output I/F</text>\n',
                        '<text top="799" left="370" width="60" height="19" font="8">USB 3.0 </text>\n',
                        '<text top="826" left="230" width="124" height="19" font="7">Output Connector</text>\n',
                        '<text top="826" left="370" width="126" height="19" font="8">19 Pin box header</text>\n',
                        '<text top="853" left="325" width="29" height="19" font="7">TDP</text>\n',
                        '<text top="853" left="370" width="159" height="19" font="8">1.12W (3.3V x 340mA)</text>\n',
                        '<text top="881" left="215" width="138" height="19" font="7">Dimension (WxLxH)</text>\n',
                        '<text top="881" left="370" width="158" height="19" font="8">30.0 x 50.9 x 8.45 mm</text>\n',
                        '<text top="918" left="263" width="90" height="19" font="7">Temperature</text>\n',
                        '<text top="908" left="370" width="126" height="19" font="8">Operation: STD: 0</text>\n',
                        '<text top="911" left="497" width="4" height="16" font="9">°</text>\n',
                        '<text top="908" left="501" width="59" height="19" font="8">C ~ +70</text>\n',
                        '<text top="911" left="560" width="4" height="16" font="9">°</text>\n',
                        '<text top="908" left="564" width="82" height="19" font="8">C. W/T: -40</text>\n',
                        '<text top="911" left="645" width="4" height="16" font="9">°</text>\n',
                        '<text top="908" left="649" width="59" height="19" font="8">C ~ +85</text>\n',
                        '<text top="911" left="709" width="4" height="16" font="9">°</text>\n',
                        '<text top="908" left="712" width="10" height="19" font="8">C</text>\n',
                        '<text top="927" left="370" width="87" height="19" font="8">Storage: -55</text>\n',
                        '<text top="930" left="457" width="4" height="16" font="9">°</text>\n',
                        '<text top="927" left="461" width="59" height="19" font="8">C ~ +95</text>\n',
                        '<text top="930" left="521" width="4" height="16" font="9">°</text>\n',
                        '<text top="927" left="524" width="10" height="19" font="8">C</text>\n',
                        '<text top="954" left="265" width="88" height="19" font="7">Environment</text>\n',
                        '<text top="954" left="370" width="343" height="19" font="8">Vibration: 5G @7~2000Hz, Shock: 50G @ 0.5ms </text>\n',
                        '<text top="1020" left="314" width="40" height="19" font="7">Notes</text>\n',
                        '<text top="982" left="370" width="344" height="19" font="8">Please download driver from MyInnodisk website.</text>\n',
                        '<text top="1001" left="370" width="278" height="19" font="8">Windows: XP(32 bit), 7(32/64 bit), Vista</text>\n',
                        '<text top="1020" left="370" width="202" height="19" font="8">Linux: Kernel v2.6.0, v2.6.8  </text>\n',
                        '<text top="1039" left="370" width="382" height="19" font="8">*After Win8 and Linux Kernel v2.6.31 supports built-in </text>\n',
                        '<text top="1058" left="370" width="66" height="19" font="8">xHCI 1.0.</text>\n',
                        '<text top="57" left="150" width="417" height="29" font="10"><b>mPCIe to four USB 3.0 Module </b></text>\n',
                        '<text top="136" left="397" width="403" height="18" font="11">−Support 4 x USB 3.0 ports up to SuperSpeed (5Gbps) data </text>\n',
                        '<text top="152" left="406" width="257" height="18" font="11">rate (share PCIe Gen2 x1 bandwidth). </text>\n',
                        '<text top="172" left="397" width="389" height="18" font="11">−Independent 1.5A overcurrent protection (OCP) for each </text>\n',
                        '<text top="188" left="406" width="31" height="18" font="11">port.</text>\n',
                        '<text top="208" left="397" width="293" height="18" font="11">−Compliant with xHCI 1.0, USB 3.0 Rev 1.0.</text>\n',
                        '<text top="227" left="397" width="390" height="18" font="11">−Two USB ports from CN1 provides limited power natively.</text>\n',
                        '<text top="247" left="397" width="328" height="18" font="11">−Two USB ports from CN2 needs external power.</text>\n',
                        '<text top="267" left="397" width="394" height="18" font="11">−Supports USB Battery Charging Specification Revision 1.2.</text>\n',
                        '<text top="286" left="397" width="256" height="18" font="11">−Optional Industrial Temperature (-40</text>\n',
                        '<text top="286" left="652" width="6" height="17" font="12">°</text>\n',
                        '<text top="286" left="658" width="59" height="18" font="11">C to +85</text>\n',
                        '<text top="286" left="717" width="6" height="17" font="12">°</text>\n',
                        '<text top="286" left="723" width="79" height="18" font="11">C) support. </text>\n',
                        '<text top="307" left="397" width="253" height="18" font="11">−30µ golden finger, 3 years warranty.</text>\n',
                        '<text top="326" left="397" width="350" height="18" font="11">−Industrial design, manufactured in innodisk Taiwan</text>\n',
                        '<text top="19" left="150" width="195" height="36" font="13"><b>EMPU-3401</b></text>\n',
                        '<text top="1088" left="186" width="186" height="22" font="6"><b>Order Information</b></text>\n',
                        '<text top="1109" left="208" width="260" height="19" font="14"><b>EMPU-3401-C1(Standard Temp.)</b></text>\n',
                        '<text top="1128" left="208" width="233" height="19" font="14"><b>EMPU-3401-W1(Wide Temp.)</b></text>\n',
                        '<text top="1147" left="208" width="218" height="19" font="15">mPCIe to four USB 3.0 Module </text>\n',
                        '<text top="170" left="196" width="141" height="15" font="16">USB 3.0 Box header (CN1)</text>\n',
                        '<text top="116" left="251" width="48" height="15" font="16">Power In</text>\n',
                        '<text top="143" left="241" width="68" height="11" font="17">5V GND GND 5V </text>\n',
                        '<text top="200" left="197" width="141" height="15" font="16">USB 3.0 Box header (CN2)</text>\n',
                        '<text top="418" left="579" width="111" height="13" font="18">USB 3.0 Pin Assignment</text>\n',
                        '<text top="438" left="540" width="27" height="13" font="18">Signal</text>\n',
                        '<text top="438" left="612" width="14" height="13" font="18">Pin</text>\n',
                        '<text top="438" left="647" width="14" height="13" font="18">Pin</text>\n',
                        '<text top="438" left="703" width="27" height="13" font="18">Signal</text>\n',
                        '<text top="455" left="543" width="22" height="13" font="18">Vbus</text>\n',
                        '<text top="454" left="615" width="7" height="15" font="19">1</text>\n',
                        '<text top="471" left="519" width="70" height="13" font="18">IntA_P1_SSRX-</text>\n',
                        '<text top="470" left="615" width="7" height="15" font="19">2</text>\n',
                        '<text top="470" left="647" width="13" height="15" font="19">19</text>\n',
                        '<text top="471" left="705" width="22" height="13" font="18">Vbus</text>\n',
                        '<text top="486" left="517" width="74" height="13" font="18">IntA_P1_SSRX+</text>\n',
                        '<text top="485" left="615" width="7" height="15" font="19">3</text>\n',
                        '<text top="485" left="647" width="13" height="15" font="19">18</text>\n',
                        '<text top="486" left="681" width="70" height="13" font="18">IntA_P1_SSRX-</text>\n',
                        '<text top="502" left="543" width="21" height="13" font="18">GND</text>\n',
                        '<text top="501" left="615" width="7" height="15" font="19">4</text>\n',
                        '<text top="501" left="647" width="13" height="15" font="19">17</text>\n',
                        '<text top="502" left="680" width="74" height="13" font="18">IntA_P2_SSRX+</text>\n',
                        '<text top="519" left="519" width="70" height="13" font="18">IntA_P1_SSTX-</text>\n',
                        '<text top="518" left="615" width="7" height="15" font="19">5</text>\n',
                        '<text top="518" left="647" width="13" height="15" font="19">16</text>\n',
                        '<text top="519" left="706" width="21" height="13" font="18">GND</text>\n',
                        '<text top="536" left="517" width="74" height="13" font="18">IntA_P1_SSTX+</text>\n',
                        '<text top="535" left="615" width="7" height="15" font="19">6</text>\n',
                        '<text top="535" left="647" width="13" height="15" font="19">15</text>\n',
                        '<text top="536" left="682" width="70" height="13" font="18">IntA_P2_SSTX-</text>\n',
                        '<text top="553" left="543" width="21" height="13" font="18">GND</text>\n',
                        '<text top="552" left="615" width="7" height="15" font="19">7</text>\n',
                        '<text top="552" left="647" width="13" height="15" font="19">14</text>\n',
                        '<text top="553" left="680" width="74" height="13" font="18">IntA_P2_SSTX+</text>\n',
                        '<text top="570" left="527" width="53" height="13" font="18">IntA_P1_D-</text>\n',
                        '<text top="569" left="615" width="7" height="15" font="19">8</text>\n',
                        '<text top="569" left="647" width="13" height="15" font="19">13</text>\n',
                        '<text top="570" left="706" width="21" height="13" font="18">GND</text>\n',
                        '<text top="587" left="525" width="57" height="13" font="18">IntA_P1_D+</text>\n',
                        '<text top="586" left="615" width="7" height="15" font="19">9</text>\n',
                        '<text top="586" left="647" width="13" height="15" font="19">12</text>\n',
                        '<text top="587" left="690" width="53" height="13" font="18">IntA_P2_D-</text>\n',
                        '<text top="605" left="612" width="13" height="15" font="19">10</text>\n',
                        '<text top="605" left="647" width="13" height="15" font="19">11</text>\n',
                        '<text top="606" left="688" width="57" height="13" font="18">IntA_P2_D+</text>\n',
                        '<text top="248" left="223" width="98" height="15" font="16">20cm Power Cable</text>\n',
                        '<text top="328" left="227" width="87" height="15" font="16">25cm USB Cable</text>\n',
                    ],
                ),
                "2": PageData(
                    size=PageSize(top=0.0, left=0.0, height=1170.0, width=810.0),
                    data=[
                        '<text top="1136" left="619" width="160" height="18" font="0"><b>www.innodisk.com</b></text>\n',
                        '<text top="37" left="151" width="637" height="33" font="20"><b>How to Unplug USB 3.0 19pin Connectors </b></text>\n',
                        '<text top="69" left="151" width="241" height="33" font="20"><b>from Mainboard</b></text>\n',
                        '<text top="117" left="48" width="728" height="18" font="21">The USB 3.0 19pin connector is a standard connector that is not designed for multi-times plug/unplug usage. </text>\n',
                        '<text top="135" left="48" width="728" height="18" font="21">The purpose of the USB 3.0 19pin connector is to securely connect when the cable is plugged in, not to allow </text>\n',
                        '<text top="153" left="48" width="716" height="18" font="21">users to unplug easily. Therefore, there are small tabs located on the cable connector that clips into the pin </text>\n',
                        '<text top="171" left="48" width="224" height="18" font="21">header connector from the inside.</text>\n',
                        '<text top="449" left="46" width="718" height="18" font="21">To pull off the USB 3.0 cable, DO NOT unplug the USB cable from the module directly, Wiggle Left- Right to </text>\n',
                        '<text top="467" left="46" width="655" height="18" font="21">release the small tabs from sockets then unplug the cable, refer to the below pictures for example:</text>\n',
                    ],
                ),
                "3": PageData(
                    size=PageSize(top=0.0, left=0.0, height=1170.0, width=810.0),
                    data=[
                        '<text top="1136" left="619" width="160" height="18" font="0"><b>www.innodisk.com</b></text>\n',
                        '<text top="36" left="151" width="396" height="36" font="13"><b>Performance Reference</b></text>\n',
                        '<text top="108" left="245" width="232" height="29" font="10"><b>One USB 3.0 Port</b></text>\n',
                        '<text top="602" left="242" width="240" height="29" font="10"><b>Four USB 3.0 Port</b></text>\n',
                    ],
                ),
            }
        )

        self.converted_data = TransformData(
            pages={
                1: PageGenerate(
                    data={
                        1: {
                            "Top": {
                                "Text": [
                                    {
                                        "text": "<b>EMPU-3401</b>",
                                        "top": 19,
                                        "left": 150,
                                        "width": 195,
                                        "height": 36,
                                        "font": 13,
                                    },
                                    {
                                        "text": "<b>mPCIe to four USB 3.0 Module </b>",
                                        "top": 57,
                                        "left": 150,
                                        "width": 417,
                                        "height": 29,
                                        "font": 10,
                                    },
                                ]
                            },
                            "Features": {
                                "Text": [
                                    {
                                        "text": "<b>−Two USB ports from CN1 provides limited power natively.</b>",
                                        "top": 200,
                                        "left": 197,
                                        "width": 141,
                                        "height": 15,
                                        "font": 16,
                                    },
                                    {
                                        "text": "<b>−Two USB ports from CN2 needs external power.</b>",
                                        "top": 208,
                                        "left": 397,
                                        "width": 293,
                                        "height": 18,
                                        "font": 11,
                                    },
                                ]
                            },
                            "MechanicalDrawing": {
                                "Text": [
                                    {
                                        "text": "<b>Mechanical Drawing</b>",
                                        "top": 501,
                                        "left": 615,
                                        "width": 7,
                                        "height": 15,
                                        "font": 19,
                                    },
                                    {
                                        "text": "<b>25cm USB Cable</b>",
                                        "top": 518,
                                        "left": 615,
                                        "width": 7,
                                        "height": 15,
                                        "font": 18,
                                    },
                                ]
                            },
                            "Specifications": {
                                "Text": [
                                    {
                                        "text": "<b>4</b>",
                                        "top": 519,
                                        "left": 615,
                                        "width": 21,
                                        "height": 13,
                                        "font": 18,
                                    },
                                    {
                                        "text": "<b>17</text>",
                                        "top": 520,
                                        "left": 543,
                                        "width": 53,
                                        "height": 15,
                                    },
                                ]
                            },
                        },
                        2: {
                            "Headquarters": {
                                "text": [
                                    {
                                        "top": 735,
                                        "left": 22,
                                        "width": 126,
                                        "height": 13,
                                        "font": 1,
                                    },
                                    {
                                        "top": 744,
                                        "left": 268,
                                        "width": 85,
                                        "height": 19,
                                        "font": 7,
                                    },
                                    {
                                        "top": 744,
                                        "left": 370,
                                        "width": 46,
                                        "height": 19,
                                        "font": 8,
                                    },
                                ]
                            },
                            "Form-Factor": [
                                {
                                    "top": 744,
                                    "left": 22,
                                    "width": 85,
                                    "height": 19,
                                    "font": 7,
                                }
                            ],
                            "mPCIe": [
                                {
                                    "top": 751,
                                    "left": 22,
                                    "width": 154,
                                    "height": 13,
                                    "font": 2,
                                },
                                {
                                    "top": 764,
                                    "left": 22,
                                    "width": 152,
                                    "height": 13,
                                    "font": 2,
                                },
                                {
                                    "top": 771,
                                    "left": 291,
                                    "width": 62,
                                    "height": 19,
                                    "font": 7,
                                },
                            ],
                            "5F., No.237, Sec. 1, Datong Rd., Xizhi Dist., New Taipei City 221": [
                                {
                                    "top": 864,
                                    "left": 32,
                                    "width": 82,
                                    "height": 13,
                                    "font": 2,
                                }
                            ],
                            "Xizhi Dist., New Taipei City 221, Taiwan": [
                                {
                                    "top": 771,
                                    "left": 291,
                                    "width": 62,
                                    "height": 19,
                                    "font": 7,
                                },
                                {
                                    "top": 771,
                                    "left": 370,
                                    "width": 114,
                                    "height": 19,
                                    "font": 8,
                                },
                            ],
                            "Taiwan": [
                                {
                                    "top": 776,
                                    "left": 22,
                                    "width": 33,
                                    "height": 13,
                                    "font": 2,
                                },
                                {
                                    "top": 789,
                                    "left": 22,
                                    "width": 113,
                                    "height": 13,
                                    "font": 2,
                                },
                            ],
                            "Tel: +886-2-7703-3000": [
                                {
                                    "top": 799,
                                    "left": 280,
                                    "width": 73,
                                    "height": 19,
                                    "font": 7,
                                },
                                {
                                    "top": 799,
                                    "left": 370,
                                    "width": 60,
                                    "height": 19,
                                    "font": 8,
                                },
                            ],
                            "USB 3.0": [
                                {
                                    "top": 802,
                                    "left": 22,
                                    "width": 124,
                                    "height": 13,
                                    "font": 2,
                                },
                                {
                                    "top": 823,
                                    "left": 22,
                                    "width": 80,
                                    "height": 13,
                                    "font": 1,
                                },
                            ],
                            "Email: sales@innodisk.com": [
                                {
                                    "top": 826,
                                    "left": 230,
                                    "width": 124,
                                    "height": 19,
                                    "font": 7,
                                },
                                {
                                    "top": 826,
                                    "left": 370,
                                    "width": 126,
                                    "height": 19,
                                    "font": 8,
                                },
                            ],
                            "Branch Offices": [
                                {
                                    "top": 826,
                                    "left": 230,
                                    "width": 124,
                                    "height": 19,
                                    "font": 7,
                                },
                                {
                                    "top": 826,
                                    "left": 370,
                                    "width": 126,
                                    "height": 19,
                                    "font": 8,
                                },
                            ],
                            "USA": [
                                {
                                    "top": 839,
                                    "left": 22,
                                    "width": 22,
                                    "height": 13,
                                    "font": 1,
                                },
                                {
                                    "top": 851,
                                    "left": 32,
                                    "width": 108,
                                    "height": 13,
                                    "font": 3,
                                },
                            ],
                            "TDP": [
                                {
                                    "top": 853,
                                    "left": 325,
                                    "width": 29,
                                    "height": 19,
                                    "font": 7,
                                },
                                {
                                    "top": 853,
                                    "left": 370,
                                    "width": 159,
                                    "height": 19,
                                    "font": 8,
                                },
                            ],
                            "China": [
                                {
                                    "top": 902,
                                    "left": 22,
                                    "width": 30,
                                    "height": 13,
                                    "font": 1,
                                },
                                {
                                    "top": 954,
                                    "left": 265,
                                    "width": 88,
                                    "height": 19,
                                    "font": 7,
                                },
                            ],
                            "Email: sales@innodisk.com (eusales@innodisk.com)": [
                                {
                                    "top": 952,
                                    "left": 22,
                                    "width": 30,
                                    "height": 13,
                                    "font": 1,
                                },
                                {
                                    "top": 954,
                                    "left": 370,
                                    "width": 344,
                                    "height": 19,
                                    "font": 8,
                                },
                            ],
                            "mPCIe to four USB 3.0 Module": [
                                {
                                    "top": 1136,
                                    "left": 619,
                                    "width": 160,
                                    "height": 18,
                                    "font": 0,
                                },
                                {
                                    "top": 1147,
                                    "left": 208,
                                    "width": 218,
                                    "height": 19,
                                    "font": 15,
                                },
                            ],
                        },
                    }
                ),
                2: PageGenerate(
                    data={
                        1: {
                            "TopTexts": [
                                {
                                    "textId": 0,
                                    "top": 37,
                                    "left": 151,
                                    "width": 637,
                                    "height": 33,
                                    "font": 20,
                                },
                                {
                                    "textId": 1,
                                    "top": 69,
                                    "left": 151,
                                    "width": 241,
                                    "height": 33,
                                    "font": 20,
                                },
                            ],
                            "MiddleTexts": [
                                {
                                    "textId": 2,
                                    "top": 117,
                                    "left": 48,
                                    "width": 728,
                                    "height": 18,
                                    "font": 21,
                                },
                                {
                                    "textId": 3,
                                    "top": 135,
                                    "left": 48,
                                    "width": 728,
                                    "height": 18,
                                    "font": 21,
                                },
                            ],
                            "BottomTexts": [
                                {
                                    "textId": 4,
                                    "top": 153,
                                    "left": 48,
                                    "width": 716,
                                    "height": 18,
                                    "font": 21,
                                },
                                {
                                    "textId": 5,
                                    "top": 171,
                                    "left": 48,
                                    "width": 224,
                                    "height": 18,
                                    "font": 21,
                                },
                            ],
                            "BottomSeparatorText": {
                                "textId": 6,
                                "top": 449,
                                "left": 46,
                                "width": 718,
                                "height": 18,
                                "font": 21,
                            },
                            "MiddleSeparatorText": {
                                "textId": 7,
                                "top": 467,
                                "left": 46,
                                "width": 655,
                                "height": 18,
                                "font": 21,
                            },
                        },
                        2: {
                            "table_of_contents": {
                                "section1": {"top": 10, "left": 20},
                                "section2": {"top": 50, "left": 100},
                            }
                        },
                    }
                ),
                3: PageGenerate(
                    data={
                        1: {
                            "Performance Reference": {
                                "top": 36,
                                "left": 151,
                                "width": 396,
                                "height": 36,
                            },
                            "One USB 3.0 Port": {
                                "top": 108,
                                "left": 245,
                                "width": 232,
                                "height": 29,
                                "font": 10,
                            },
                            "Four USB 3.0 Port": {
                                "top": 602,
                                "left": 242,
                                "width": 240,
                                "height": 29,
                                "font": 10,
                            },
                        },
                        2: {
                            "text": [
                                {
                                    "top": 1136,
                                    "left": 619,
                                    "width": 160,
                                    "height": 18,
                                    "font": 0,
                                },
                                {
                                    "top": None,
                                    "left": 1136,
                                    "width": 159,
                                    "height": 19,
                                    "font": 0,
                                },
                            ]
                        },
                    }
                ),
            }
        )

    def test_get_str_similarity(self):
        metric, setting = SimilarityMetrics.get("str_similarity")
        self.assertTrue(callable(metric), "Metric is callable")
        self.assertIsInstance(setting, dict, "Setting should be a dictionary")

    def test_evaluator(self):
        metric, setting = SimilarityMetrics.get("str_similarity")

        eval = Validate(
            metrics=metric,
            setting=setting,
        )

        score = eval.process(gt_data=self.gt_data, data=self.converted_data)

        self.assertIsInstance(score, Scores)
        self.assertEqual(len(score.pages), 4, "Data should not be empty")


if __name__ == "__main__":
    unittest.main()
