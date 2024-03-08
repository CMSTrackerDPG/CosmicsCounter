import time

def generate_html(year, allAlcaTracks_currentCRUZET, allTime_currentCRUZET, mincruzetrunforstat, maxcruzetrunforstat, allAlcaTracks_pix_currentCRUZET, allTime_pix_currentCRUZET, mincruzetrunforstat_pix, maxcruzetrunforstat_pix, allAlcaTracks_currentCRAFT, allTime_currentCRAFT, mincosmicrunforstat, maxcosmicrunforstat, allAlcaTracks_pix_currentCRAFT, allTime_pix_currentCRAFT, mincosmicrunforstat_pix, maxcosmicrunforstat_pix):
    
    htmlCOSMICTRACKS = """
    <!DOCTYPE html>
    <html lang="en">
     <head>
       <meta charset="utf-8">
         <meta name="viewport" content="width=device-width, initial-scale=1">
         <title>Cosmic Tracks Summary</title>
          <!-- Bootstrap -->
         <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
          <!-- Main Style -->
         <link rel="stylesheet" type="text/css" href="css/main.css">
         <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
         <script>
           function apri(url) {
             newin = window.open(url,'titolo','scrollbars=no,resizable=yes, width=1300,height=700,status=no,location=no,toolbar=no');
           }
         </script>
       </head>
      <body>
     <section id="text-about">
         %s ALCARECO cosmic tracks (%s)
     </section>
     <!--------------------------------------------------------------------------------->
     <div id="myModal" class="modal">
       <!-- Modal content -->
       <div class="modal-content">
         <span class="close">&times;</span>
         <p style="text-align: center; width: 100%%;"><a id="pngLink" href="#" download="">Download PNG</a></p>
         <div id="trend" style="justify-content: center; width: 99%%; aspect-ratio: 9 / 4"></div>
       </div>
     </div>
     <!--------------------------------------------------------------------------------->
     <section id="my-table">
         <div class="container">
              <div class="row">
                 <div class="main">
                      <div class="col-lg-5 col-md-5 col-sm-12 col-xs-12">
                         <div class="my-table">
                             <div class="table-header">
                               <p class="table-title">CRUZET</p>
                                 <p class="table-sep"><hr style="border: 4px solid white; width: 95%%;" /></p>
                                 <p class="table-mytxt">ALCA tracks: <span class="table-tracks">%.0fK</span></p>
                                 <p class="table-counts">Time: %i hours&nbsp;&nbsp;&nbsp; Run range: %i / %i</p>
                                 <p class="table-mylink">Plots:<a style="padding-left: 10px; padding-right: 10px;" id="cruzetTrend" href="#">Trend</a><a style="padding-right: 10px;" id="cruzetRate" href="#">Rate</a><a style="padding-right: 10px;" id="cruzetCumul" href="#">Cumulative</a><a href="javascript:apri('./cruzet.html');">All</a></p>
                                 <p class="table-sep"><hr style="border: 1px dashed white; width: 70%%;" /></p>
                                 <p class="table-mytxt">ALCA Pixel tracks: <span class="table-tracks">%.0fK</span></p>
                                 <p class="table-counts">Time: %i hours&nbsp;&nbsp;&nbsp; Run range: %i / %i</p>
                                 <p class="table-mylink">Plots:<a style="padding-left: 10px; padding-right: 10px;" id="cruzetTrendp" href="#">Trend</a><a style="padding-right: 10px;" id="cruzetRatep" href="#">Rate</a><a style="padding-right: 10px;" id="cruzetCumulp" href="#">Cumulative</a><a href="javascript:apri('./cruzet_pixel.html');">All</a></p>
                             </div>
                         </div>
                     </div>
                      <div class="col-lg-2 col-md-2 col-sm-0 col-xs-0"></div>
                        <div class="col-lg-5 col-md-5 col-sm-12 col-xs-12">
                         <div class="my-table">
                             <div class="table-header">
                                 <p class="table-title">CRAFT</p>
                                 <p class="table-sep"><hr style="border: 4px solid white; width: 95%%;" /></p>
                                 <p class="table-mytxt">ALCA tracks: <span class="table-tracks">%.0fK</span></p>
                                 <p class="table-counts">Time: %i hours&nbsp;&nbsp;&nbsp; Run range: %i / %i</p>
                                 <p class="table-mylink">Plots:<a style="padding-left: 10px; padding-right: 10px;" id="craftTrend" href="#">Trend</a><a style="padding-right: 10px;" id="craftRate" href="#">Rate</a><a id="craftCumul" style="padding-right: 10px;" href="#">Cumulative</a><a href="javascript:apri('./craft.html');">All</a></p>
                                 <p class="table-sep"><hr style="border: 1px dashed white; width: 70%%;" /></p>
                                 <p class="table-mytxt">ALCA Pixel tracks: <span class="table-tracks">%.0fK</span></p>
                                 <p class="table-counts">Time: %i hours&nbsp;&nbsp;&nbsp; Run range: %i / %i</p>
                                 <p class="table-mylink">Plots:<a style="padding-left: 10px; padding-right: 10px;" id="craftTrendp" href="#">Trend</a><a style="padding-right: 10px;" id="craftRatep" href="#">Rate</a><a id="craftCumulp" style="padding-right: 10px;" href="#">Cumulative</a><a href="javascript:apri('./craft_pixel.html');">All</a></p>
                             </div>
                         </div>
                     </div>
                   </div>
             </div>
          </div>
     </section>
    </body>
    <script type='module'>
     import { openFile, draw } from 'https://root.cern/js/latest/modules/main.mjs';
     import {loadModal} from './js/modalFun.js';
     let file = await openFile('./data/cosmics.root');
     let obj = []
     obj.push(await file.readObject('c_CRUZET;1'));
     obj.push(await file.readObject('c_CRUZET_rate;1'));
     obj.push(await file.readObject('c_CRUZET_cumul;1'));
     obj.push(await file.readObject('c_CRUZET_p;1'));
     obj.push(await file.readObject('c_CRUZET_p_rate;1'));
     obj.push(await file.readObject('c_CRUZET_p_cumul;1'));
     obj.push(await file.readObject('c_CRAFT;1'));
     obj.push(await file.readObject('c_CRAFT_rate;1'));
     obj.push(await file.readObject('c_CRAFT_cumul;1'));
     obj.push(await file.readObject('c_CRAFT_p;1'));
     obj.push(await file.readObject('c_CRAFT_p_rate;1'));
     obj.push(await file.readObject('c_CRAFT_p_cumul;1'));
     $( document ).ready(function() {
         loadModal(obj);
     });
   </script>
  </html>
""" % (year,time.ctime(), allAlcaTracks_currentCRUZET / 1000., abs(allTime_currentCRUZET / 3600), mincruzetrunforstat, maxcruzetrunforstat, allAlcaTracks_pix_currentCRUZET / 1000., abs(allTime_pix_currentCRUZET / 3600), mincruzetrunforstat_pix, maxcruzetrunforstat_pix, allAlcaTracks_currentCRAFT / 1000., abs(allTime_currentCRAFT / 3600), mincosmicrunforstat, maxcosmicrunforstat, allAlcaTracks_pix_currentCRAFT / 1000., abs(allTime_pix_currentCRAFT / 3600), mincosmicrunforstat_pix, maxcosmicrunforstat_pix)

    outCOSMICTRACKS = open("index.html", "w")
    outCOSMICTRACKS.write(htmlCOSMICTRACKS)
    outCOSMICTRACKS.close()


