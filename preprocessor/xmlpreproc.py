import xml.etree.ElementTree as ET
from typing import List, Tuple

from preprocessor.core import BasePreprocessor


class XMLPreProcessor(BasePreprocessor):
    def sort_text_elements(
        self, xml_text_lines: List[str], descending: bool = False
    ) -> List[str]:
        """
        Sorts a list of <text> XML strings by their 'top' attribute.

        Args:
            xml_text_lines (List[str]): List of <text> XML strings.
            descending (bool): If True, sort from bottom to top. Default: False (top to bottom).

        Returns:
            List[str]: Sorted <text> elements as strings.

        Raises:
            Exception: An error occurred while sort text elements.
        """
        try:
            parsed = []
            for xml_str in xml_text_lines:
                try:
                    elem = ET.fromstring(xml_str)
                    if elem.tag != "text":
                        continue
                    top = int(elem.attrib.get("top", 0))
                    parsed.append((top, xml_str))
                except ET.ParseError:
                    continue

            parsed.sort(key=lambda item: item[0], reverse=descending)
            return [xml for _, xml in parsed]
        except Exception as e:
            raise e

    def deduplicate_text_elements_from_strings(
        self, xml_text_lines: List[str], top_tolerance: int = 5, left_tolerance: int = 5
    ) -> List[str]:
        """
        Remove duplicate text elements from a list of XML text lines based on spatial tolerance.

        This function compares text elements by their position attributes (e.g., top and left)
        and removes entries that are within a given tolerance range, treating them as duplicates.

        Args:
            xml_text_lines (List[str]): A list of XML strings representing individual text elements.
            top_tolerance (int, optional): The vertical threshold (in pixels or units) for determining duplicates. Defaults to 5.
            left_tolerance (int, optional): The horizontal threshold for determining duplicates. Defaults to 5.

        Returns:
            List[str]: A list of deduplicated XML text elements as strings.

        Raises:
            Exception:
                An error occurred while deduplicate text elements.
        """
        try:
            seen = []
            unique_elements = []

            for line in xml_text_lines:
                try:
                    elem = ET.fromstring(line)
                    if elem.tag != "text":
                        continue
                    content = "".join(elem.itertext()).strip()
                    top = int(elem.attrib.get("top", "0"))
                    left = int(elem.attrib.get("left", "0"))

                    # Compare duplicate：similar context + close location（top / left）
                    duplicate = False
                    for item in seen:
                        if (
                            content == item["content"]
                            and abs(top - item["top"]) <= top_tolerance
                            and abs(left - item["left"]) <= left_tolerance
                        ):
                            duplicate = True
                            break

                    if not duplicate:
                        seen.append({"content": content, "top": top, "left": left})
                        unique_elements.append(line)
                except ET.ParseError:
                    continue

            return unique_elements
        except Exception as e:
            raise e

    def split_texts_by_center_segment(
        self,
        xml_text_lines: List[str],
    ) -> Tuple[List[str], List[str]]:
        """
        Splits a list of XML strings into two segments based on the center of the text elements.

        Args:
            xml_text_lines (List[str]): List of XML strings representing text elements.

        Returns:
            Tuple[List[str], List[str]]: Two lists of XML strings, upper data and lower data.

        Raises:
            An error occurred while split texts by center segment.
        """
        try:
            parsed = []
            for line in xml_text_lines:
                try:
                    elem = ET.fromstring(line)
                    if elem.tag != "text":
                        continue
                    top = int(elem.attrib.get("top", 0))
                    is_bold = "b" in "".join(child.tag for child in elem.iter())
                    parsed.append({"top": top, "line": line, "is_bold": is_bold})
                except:
                    continue

            if not parsed:
                return [], []

            max_top = parsed[-1]["top"]
            center_y = max_top // 2
            closest = min(parsed, key=lambda x: abs(x["top"] - center_y))
            center_idx = parsed.index(closest)

            if closest["is_bold"]:
                for i in range(center_idx - 1, -1, -1):
                    if not parsed[i]["is_bold"]:
                        split_top = parsed[i]["top"]
                        break
                else:
                    split_top = closest["top"]
            else:
                for i in range(center_idx + 1, len(parsed)):
                    if parsed[i]["is_bold"]:
                        split_top = parsed[i]["top"]
                        break
                else:
                    split_top = closest["top"]

            upper_data = [x["line"] for x in parsed if x["top"] <= split_top]
            lower_data = [x["line"] for x in parsed if x["top"] > split_top]

            return upper_data, lower_data
        except Exception as e:
            raise Exception(
                f"An error occurred while split texts by center segment: {e}"
            ) from e

    # TODO : In future work, we plan to support options for users to: (1) deduplicate text elements, and (2) split text by center into two segments per page.
    # TODO : need a reader to the output data.
    def process(self, data: dict) -> dict:
        """
        Process the XML data to remove duplicates and sort by 'top' attribute.
        Args:
            data (dict): A dictionary containing XML text elements.

        Returns:
            dict: A dictionary with pages as keys and two segments of text elements as values.

        Raises:
            ValueError: Expected a list of text elements for page.
            Exception: An error occurred while processing the data.
        """
        pages_data = {}
        try:
            for page, text_elements in data.items():
                if not isinstance(text_elements, list):
                    raise ValueError(
                        f"Expected a list of text elements for page {page}."
                    )

                # Sort by 'top' attribute
                sorted_elements = self.sort_text_elements(text_elements)

                # Remove duplicates
                unique_elements = self.deduplicate_text_elements_from_strings(
                    sorted_elements
                )

                # Split into two segments
                upper_data, lower_data = self.split_texts_by_center_segment(
                    unique_elements
                )
                pages_data.update({page: {0: upper_data, 1: lower_data}})
            return pages_data
        except Exception as e:
            raise Exception(f"An error occurred while processing the file: {e}")


if __name__ == "__main__":
    data = {
        "1": [
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
        "2": [
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
        "3": [
            '<text top="1136" left="619" width="160" height="18" font="0"><b>www.innodisk.com</b></text>\n',
            '<text top="36" left="151" width="396" height="36" font="13"><b>Performance Reference</b></text>\n',
            '<text top="108" left="245" width="232" height="29" font="10"><b>One USB 3.0 Port</b></text>\n',
            '<text top="602" left="242" width="240" height="29" font="10"><b>Four USB 3.0 Port</b></text>\n',
        ],
    }
    xml_preprocessor = XMLPreProcessor()
    preprocessed_data = xml_preprocessor.process(data)
    for page in preprocessed_data:
        upper_data, lower_data = preprocessed_data[page]
        print(
            preprocessed_data[page][upper_data],
            "\n***************\n",
            preprocessed_data[page][lower_data],
        )
        print(f"\n{'-' * 50}\n")
