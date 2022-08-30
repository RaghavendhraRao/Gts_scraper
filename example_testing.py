from bs4 import BeautifulSoup, NavigableString
import html_text



html = """
<div class="panel-body"> 
        <div>
         <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="">Level : 1 | </font><font style="vertical-align: inherit;" class="">Semester : 1 - 95. Architecture</font></font></label>
        </div> 
        <table style="border-collapse:collapse;padding-bottom:5px; width: 100%;margin-bottom:10px !important" cellspacing="3" cellpadding="0" border="0"> 
         <thead> 
          <tr> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Course Code</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Course Name</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Core/Elective</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;" nowrap=""><font style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="">Theory+Practice (Hour)</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ECTS</font></font></th> 
          </tr> 
         </thead> 
         <tbody> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760370&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 103</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Architectural Drawing I</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="">3+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760382&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 111</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Basic Design I</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8+3</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760444&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 179</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="">History of Cultures and Ideas</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760410&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">FA 113</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Design Geometry</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760714&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">FA/E 179</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">English for Academic Purposes I</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14758269&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">TK 103</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Turkish Language I</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" colspan="4" style="font-weight:bold"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Total ECTS credits</font></font></td> 
           <td class="tyycCell text-center" style="font-weight:bold"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">30</font></font></td> 
          </tr> 
         </tbody> 
        </table> 
        <div>
         <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Level : 1 | </font><font style="vertical-align: inherit;">Semester : 2 - 95. Architecture</font></font></label>
        </div> 
        <table style="border-collapse:collapse;padding-bottom:5px; width: 100%;margin-bottom:10px !important" cellspacing="3" cellpadding="0" border="0"> 
         <thead> 
          <tr> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Course Code</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Course Name</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Core/Elective</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;" nowrap=""><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Theory+Practice (Hour)</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ECTS</font></font></th> 
          </tr> 
         </thead> 
         <tbody> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760371&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 104</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Architectural Drawing II</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760384&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 112</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Basic Design II</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8+3</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760449&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 180</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Introduction to Architecture</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760409&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">FA 114</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Design Computing</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760753&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">FA/E 180</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">English for Academic Purposes II</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14758273&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">TK 104</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Turkish Language II</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" colspan="4" style="font-weight:bold"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Total ECTS credits</font></font></td> 
           <td class="tyycCell text-center" style="font-weight:bold"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">30</font></font></td> 
          </tr> 
         </tbody> 
        </table> 
        <div>
         <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Level : 2 | </font><font style="vertical-align: inherit;">Semester : 1 - 95. Architecture</font></font></label>
        </div> 
        <table style="border-collapse:collapse;padding-bottom:5px; width: 100%;margin-bottom:10px !important" cellspacing="3" cellpadding="0" border="0"> 
         <thead> 
          <tr> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Course Code</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Course Name</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Core/Elective</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;" nowrap=""><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Theory+Practice (Hour)</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ECTS</font></font></th> 
          </tr> 
         </thead> 
         <tbody> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760479&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 190</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Practice in Construction and Design Technologies</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760362&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 201</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Architectural Design I</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8+3</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760388&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 211</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Building Materials and Technologies I</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760502&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 231</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Statics</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760438&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 241</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">History of Architecture I</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">..........</font></font></label> </td> 
           <td class="tyycCell"> <a href="https://ects-bilgi-edu-tr.translate.goog/Elective/Detail?catalog_electiveId=79867&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">F-ARCH List</font></font></a> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">elective</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">0+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" colspan="4" style="font-weight:bold"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Total ECTS credits</font></font></td> 
           <td class="tyycCell text-center" style="font-weight:bold"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">31</font></font></td> 
          </tr> 
         </tbody> 
        </table> 
        <div>
         <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Level : 2 | </font><font style="vertical-align: inherit;">Semester : 2 - 95. Architecture</font></font></label>
        </div> 
        <table style="border-collapse:collapse;padding-bottom:5px; width: 100%;margin-bottom:10px !important" cellspacing="3" cellpadding="0" border="0"> 
         <thead> 
          <tr> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Course Code</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Course Name</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Core/Elective</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;" nowrap=""><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Theory+Practice (Hour)</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ECTS</font></font></th> 
          </tr> 
         </thead> 
         <tbody> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760363&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 202</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Architectural Design II</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8+3</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760389&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 212</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Building Materials and Technologies II</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760503&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 232</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Strength of Materials</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760439&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 242</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">History of Architecture II</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">..........</font></font></label> </td> 
           <td class="tyycCell"> <a href="https://ects-bilgi-edu-tr.translate.goog/Elective/Detail?catalog_electiveId=79834&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">GE-Arts And Humanities List I</font></font></a> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">elective</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">0+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" colspan="4" style="font-weight:bold"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Total ECTS credits</font></font></td> 
           <td class="tyycCell text-center" style="font-weight:bold"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">29</font></font></td> 
          </tr> 
         </tbody> 
        </table> 
        <div>
         <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Level : 3 | </font><font style="vertical-align: inherit;">Semester : 1 - 95. Architecture</font></font></label>
        </div> 
        <table style="border-collapse:collapse;padding-bottom:5px; width: 100%;margin-bottom:10px !important" cellspacing="3" cellpadding="0" border="0"> 
         <thead> 
          <tr> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Course Code</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Course Name</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Core/Elective</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;" nowrap=""><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Theory+Practice (Hour)</font></font></th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ECTS</font></font></th> 
          </tr> 
         </thead> 
         <tbody> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760484&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 290</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Professional Practice I-Construction Site</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760364&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 301</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Architectural Design III</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8+3</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760483&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 309</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Production of Space and the Urban Condition</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760426&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 313</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Environment Conscious Building Design</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760440&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ARCH 341</font></font></a> </td> 
           <td class="tyycCell"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">History of Architecture III</font></font></td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">core</font></font></td> 
           <td class="tyycCell text-center"> <label><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3+0</font></font></label> </td> 
           <td class="tyycCell text-center"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760442&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">ARCH 351</a> </td> 
           <td class="tyycCell"> History of Cities </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>3+0</label> </td> 
           <td class="tyycCell text-center">4</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <label>.........</label> </td> 
           <td class="tyycCell"> <a href="https://ects-bilgi-edu-tr.translate.goog/Elective/Detail?catalog_electiveId=79867&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">F-ARCH List</a> </td> 
           <td class="tyycCell text-center"> Elective </td> 
           <td class="tyycCell text-center"> <label>0+0</label> </td> 
           <td class="tyycCell text-center">3</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" colspan="4" style="font-weight:bold">Total ECTS credits</td> 
           <td class="tyycCell text-center" style="font-weight:bold">31</td> 
          </tr> 
         </tbody> 
        </table> 
        <div>
         <label>Level : 3 | Semester : 2 - 95. Architecture</label>
        </div> 
        <table style="border-collapse:collapse;padding-bottom:5px; width: 100%;margin-bottom:10px !important" cellspacing="3" cellpadding="0" border="0"> 
         <thead> 
          <tr> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">Course Code</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">Course Name</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">Core/Elective</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;" nowrap="">Theory+Practice (Hour)</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">ECTS</th> 
          </tr> 
         </thead> 
         <tbody> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760365&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">ARCH 302</a> </td> 
           <td class="tyycCell"> Architectural Design IV </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>8+3</label> </td> 
           <td class="tyycCell text-center">10</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760456&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">ARCH 310</a> </td> 
           <td class="tyycCell"> Introduction to Urban Design </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>4+0</label> </td> 
           <td class="tyycCell text-center">4</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760497&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">ARCH 314</a> </td> 
           <td class="tyycCell"> Sensory Architecture: Light and Sound </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>4+0</label> </td> 
           <td class="tyycCell text-center">4</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <label>.........</label> </td> 
           <td class="tyycCell"> <a href="https://ects-bilgi-edu-tr.translate.goog/Elective/Detail?catalog_electiveId=79867&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">F-ARCH List</a> </td> 
           <td class="tyycCell text-center"> Elective </td> 
           <td class="tyycCell text-center"> <label>0+0</label> </td> 
           <td class="tyycCell text-center">3</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <label>.........</label> </td> 
           <td class="tyycCell"> <a href="https://ects-bilgi-edu-tr.translate.goog/Elective/Detail?catalog_electiveId=79867&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">F-ARCH List</a> </td> 
           <td class="tyycCell text-center"> Elective </td> 
           <td class="tyycCell text-center"> <label>0+0</label> </td> 
           <td class="tyycCell text-center">4</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <label>.........</label> </td> 
           <td class="tyycCell"> <a href="https://ects-bilgi-edu-tr.translate.goog/Elective/Detail?catalog_electiveId=79867&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">F-ARCH List</a> </td> 
           <td class="tyycCell text-center"> Elective </td> 
           <td class="tyycCell text-center"> <label>0+0</label> </td> 
           <td class="tyycCell text-center">4</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" colspan="4" style="font-weight:bold">Total ECTS credits</td> 
           <td class="tyycCell text-center" style="font-weight:bold">29</td> 
          </tr> 
         </tbody> 
        </table> 
        <div>
         <label>Level : 4 | Semester : 1 - 95. Architecture</label>
        </div> 
        <table style="border-collapse:collapse;padding-bottom:5px; width: 100%;margin-bottom:10px !important" cellspacing="3" cellpadding="0" border="0"> 
         <thead> 
          <tr> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">Course Code</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">Course Name</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">Core/Elective</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;" nowrap="">Theory+Practice (Hour)</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">ECTS</th> 
          </tr> 
         </thead> 
         <tbody> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760485&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">ARCH 390</a> </td> 
           <td class="tyycCell"> Professional Practice II-Architectural Office </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>1+0</label> </td> 
           <td class="tyycCell text-center">3</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760368&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">ARCH 401</a> </td> 
           <td class="tyycCell"> Architectural Design V </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>8+3</label> </td> 
           <td class="tyycCell text-center">12</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760481&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">ARCH 411</a> </td> 
           <td class="tyycCell"> Principles of Conservation and Restoration </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>6+0</label> </td> 
           <td class="tyycCell text-center">6</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760394&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">ARCH 471</a> </td> 
           <td class="tyycCell"> Codes and Regulations </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>3+0</label> </td> 
           <td class="tyycCell text-center">4</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14759888&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">HTR 111</a> </td> 
           <td class="tyycCell"> History of Turkish Revolution I </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>2+0</label> </td> 
           <td class="tyycCell text-center">2</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <label>.........</label> </td> 
           <td class="tyycCell"> <a href="https://ects-bilgi-edu-tr.translate.goog/Elective/Detail?catalog_electiveId=79867&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">F-ARCH List</a> </td> 
           <td class="tyycCell text-center"> Elective </td> 
           <td class="tyycCell text-center"> <label>0+0</label> </td> 
           <td class="tyycCell text-center">4</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" colspan="4" style="font-weight:bold">Total ECTS credits</td> 
           <td class="tyycCell text-center" style="font-weight:bold">31</td> 
          </tr> 
         </tbody> 
        </table> 
        <div>
         <label>Level : 4 | Semester : 2 - 95. Architecture</label>
        </div> 
        <table style="border-collapse:collapse;padding-bottom:5px; width: 100%;margin-bottom:10px !important" cellspacing="3" cellpadding="0" border="0"> 
         <thead> 
          <tr> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">Course Code</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">Course Name</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">Core/Elective</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;" nowrap="">Theory+Practice (Hour)</th> 
           <th class="tyycGroupCell text-center" style="background-color:transparent !important;">ECTS</th> 
          </tr> 
         </thead> 
         <tbody> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760369&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">ARCH 402</a> </td> 
           <td class="tyycCell"> Architectural Design VI </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>8+3</label> </td> 
           <td class="tyycCell text-center">14</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760501&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">ARCH 412</a> </td> 
           <td class="tyycCell"> Special Topics in Design </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>3+0</label> </td> 
           <td class="tyycCell text-center">4</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14760486&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">ARCH 472</a> </td> 
           <td class="tyycCell"> Professional Practice Management </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>3+0</label> </td> 
           <td class="tyycCell text-center">5</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <a href="https://ects-bilgi-edu-tr.translate.goog/Course/Detail?catalog_courseId=14759891&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">HTR 112</a> </td> 
           <td class="tyycCell"> History of Turkish Revolution II </td> 
           <td class="tyycCell text-center"> Core </td> 
           <td class="tyycCell text-center"> <label>2+0</label> </td> 
           <td class="tyycCell text-center">2</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" style="background-color:transparent !important;" width="120px"> <label>.........</label> </td> 
           <td class="tyycCell"> <a href="https://ects-bilgi-edu-tr.translate.goog/Elective/Detail?catalog_electiveId=84313&amp;_x_tr_sl=tr&amp;_x_tr_tl=en&amp;_x_tr_hl=en-GB&amp;_x_tr_pto=sc">Full List</a> </td> 
           <td class="tyycCell text-center"> Elective </td> 
           <td class="tyycCell text-center"> <label>0+0</label> </td> 
           <td class="tyycCell text-center">4</td> 
          </tr> 
          <tr> 
           <td class="tyycCell" colspan="4" style="font-weight:bold">Total ECTS credits</td> 
           <td class="tyycCell text-center" style="font-weight:bold">29</td> 
          </tr> 
         </tbody> 
        </table> 
        <div style="float:right"> 
         <b>Total ECTS : 240</b> 
        </div> 
       </div>
"""

soup = BeautifulSoup(html, "lxml")
print("getting soup")
tables = soup.findAll("table")
count = 0
for lable in soup.div.label.next_elements:
    print("label  ", lable.text)
for each_table in tables:
    print("table -", count)
    count +=1
    label = soup.label.next_element.text
    print("label -:", label,"\n")


# html = """
# <div class="mobileRow row mobile-toggle-content">
# <div class="mobileCell cell">
#     <div>
#     <span>
#         <strong>Degree Awarded: <span>MS</span>&nbsp;
#             <!--googleon: all-->
#             <span>Actuarial Science</span>
#         </strong>
#         <!--googleoff: all-->
#
#     </span>
#
# <div class="">
#     <!-- video and description -->
#
#         <p></p><p>The MS program in actuarial science emphasizes broad awareness and appreciation of current issues faced by insurance industry practitioners as well as innovative resolutions provided by actuaries.</p><p>Students advance their knowledge base by applying mathematical and statistical concepts and data analytics to the disciplines of risk management, finance and insurance. It also includes a new focused set of professional learning outcomes aligned with the needs of the ever-evolving insurance industry, while keeping the core technical learning outcomes in place. These guide students' development of professional competencies through coursework, independent projects and opportunities outside of the classroom, while remaining firmly based on a strong foundation of scholarly technical work in actuarial science.</p><p>Actuaries must pass a series of intensive professional exams to become credentialed. Program graduates are prepared for the examinations required to become credentialed professionals by the Society of Actuaries or Casualty Actuarial Society and to be competitive employees in the insurance and finance industries.</p><p></p>
#
# </div>
# <!--end of video-->
# <div>
#
# </div>
# </div>
# </div>
# </div>
#
# """
# import re
# regex = re.compile(r"<p/?>", re.IGNORECASE) # the filter, it finds <br> tags that may or may not have slashes
#
#
# soup = BeautifulSoup(html, "lxml")
# # print(soup)
# data = soup.find('div',{'class':"mobileCell cell"})
# a= html_text.extract_text(html)
# get_all_paragraph = soup.find_all('p')
# # newtext = re.sub(regex, '\n', data) # replaces matches with the newline
# # print(newtext)
#
# get_list = soup.find('ol').text
# for each_para in get_all_paragraph:
#     if each_para == get_all_paragraph[3]:
#         print(each_para.text+get_list)
#
# # for para in soup.findAll('li'):
# #     list[para.text] = para.text
# # print(list)
#
# # ## Degree Requirements
# # deg_title = soup.findAll('strong')
# # for title in deg_title:
# #     print(title.text)
# # for para in soup.findAll('p'):
# #     # paragraph = para.text   # total degree req
# #     try:
# #
# #         if para.text != "":
# #             if len(para.findAll('br')) > 0:
# #                 try:
# #                     degree_title = para.strong.text
# #                 except Exception as e:
# #                     degree_title = None
# #                 try:
# #
# #                     for req in para.findAll('br'):
# #                         requirement = req.next
# #                         print("title: ", degree_title, "Requiremnet: ", requirement, "\n")
# #
# #                 except Exception as e:
# #                     print("error raised while gathering req : ", e)
# #             else:
# #                 requirement = para.text
# #                 print("Requirement: ", requirement)
# #     except Exception as e:
# #         print("error raised as:", e)
#
#     # print(para)
# # print(a.text)
#
