
from ROOT import TCanvas, TLegend, TH1F, gStyle
from ROOT import kBlue, kGreen

def generate_plot(Ctype,pix,info_run_track, info_run_time, allAlcaTracks_current, allTime_current,tFile):

    tFile.cd()
    ### TXT to be displayed on all plots
    Rleg=TLegend(0.12,0.75,0.46,0.9)
    truncated_numOfTracks=allAlcaTracks_current / 1000.
    truncated_numOfTracks= "%.2f" % truncated_numOfTracks
    truncated_time=allTime_current / 3600.
    truncated_time= "%.2f" % truncated_time
    truncated_frequency = 0 if allTime_current==0 else allAlcaTracks_current /( allTime_current)
    truncated_frequency= "%.2f" % truncated_frequency
    Rleg.SetTextAlign(13)
    if pix:
        Rleg.SetHeader("#splitline{"+Ctype+" tracks: "+str(truncated_numOfTracks)+"K}{#splitline{Duration: "+str(truncated_time)+" hours}{Rate: "+str(truncated_frequency)+" Hz}}")
    else:
        Rleg.SetHeader("#splitline{"+Ctype+" Pixel tracks: "+str(truncated_numOfTracks)+"K}{#splitline{Duration: "+str(truncated_time)+" hours}{Rate: "+str(truncated_frequency)+" Hz}}")
    Rleg.SetFillStyle(0)
    Rleg.SetBorderSize(0)

    legend_info = TLegend(.45,.80,.90,.90);
    legend_info.SetTextAlign(32)
    legend_info.SetHeader("Green points are being processed. Rest is prompt reco.");
    legend_info.SetFillStyle(0)
    legend_info.SetBorderSize(0)
    legend_info.SetTextSize(0.04)


    #################
    #     TREND     #
    #################
    if pix:
        c_trend = TCanvas("c_"+Ctype+"_p","c_"+Ctype+"_p",1,1,1800,800)
    else:
        c_trend = TCanvas("c_"+Ctype,"c_"+Ctype,1,1,1800,800)
    c_trend.SetGridx(True)
    c_trend.SetGridy(True)
    
    if pix:
        trend=TH1F(Ctype+"p",Ctype+" : Number of AlCaReco Pixel tracks",len(info_run_track),0,len(info_run_track))
        trend.GetYaxis().SetTitle("# of alca pixel tracks")
        trendPNG=TH1F(Ctype+"p_PNG",Ctype+" : Number of AlCaReco Pixel tracks",len(info_run_track),0,len(info_run_track))
        trendPNG.GetYaxis().SetTitle("# of alca pixel tracks")
    else:
        trend=TH1F(Ctype,Ctype+" : Number of AlCaReco tracks",len(info_run_track),0,len(info_run_track))
        trend.GetYaxis().SetTitle("# of alca tracks")
        trendPNG=TH1F(Ctype+"_PNG",Ctype+" : Number of AlCaReco tracks",len(info_run_track),0,len(info_run_track))
        trendPNG.GetYaxis().SetTitle("# of alca tracks")        
    trend.SetFillColor(kBlue+1)
    trendPNG.SetFillColor(kBlue+1)
    
    if pix:
        trend_processing=TH1F(Ctype+"p_processing",Ctype+"p_processing",len(info_run_track),0,len(info_run_track))
    else:
        trend_processing=TH1F(Ctype+"_processing",Ctype+"_processing",len(info_run_track),0,len(info_run_track))        
    trend_processing.SetLineColor(kGreen+1)
    trend_processing.SetFillColor(kGreen+1)

    #################
    #     CUMUL     #
    #################
    if pix:
        c_cumul = TCanvas("c_"+Ctype+"_p_cumul","c_"+Ctype+"_p_cumul",1,1,1800,800)
    else:
        c_cumul = TCanvas("c_"+Ctype+"_cumul","c_"+Ctype+"_cumul",1,1,1800,800)
    c_cumul.SetGridx(True)
    c_cumul.SetGridy(True)
    
    if pix:
        cumul=TH1F(Ctype+"p_cumul",Ctype+" : Cumulative AlCaReco Pixel tracks",len(info_run_track),0,len(info_run_track))
        cumul.GetYaxis().SetTitle("cumulative sum of alca pixel tracks")
        cumulPNG=TH1F(Ctype+"p_cumulPNG",Ctype+" : Cumulative AlCaReco Pixel tracks",len(info_run_track),0,len(info_run_track))
        cumulPNG.GetYaxis().SetTitle("cumulative sum of alca pixel tracks")
    else:
        cumul=TH1F(Ctype+"_cumul",Ctype+" : Cumulative AlCaReco tracks",len(info_run_track),0,len(info_run_track))
        cumul.GetYaxis().SetTitle("cumulative sum of alca tracks")
        cumulPNG=TH1F(Ctype+"_cumulPNG",Ctype+" : Cumulative AlCaReco tracks",len(info_run_track),0,len(info_run_track))
        cumulPNG.GetYaxis().SetTitle("cumulative sum of alca tracks")        
    cumul.SetFillColor(kBlue+1)
    cumulPNG.SetFillColor(kBlue+1)
    
    if pix:
        cumul_processing=TH1F(Ctype+"p_cumul_processing",Ctype+"p_cumul_processing",len(info_run_track),0,len(info_run_track))
    else:
        cumul_processing=TH1F(Ctype+"_cumul_processing",Ctype+"_cumul_processing",len(info_run_track),0,len(info_run_track))        
    cumul_processing.SetLineColor(kGreen+1)
    cumul_processing.SetFillColor(kGreen+1)
    cumulative_tracks=0.

    #################
    #     RATE      #
    #################
    if pix:
        c_rate = TCanvas("c_"+Ctype+"_p_rate","c_"+Ctype+"_p_rate",1,1,1800,800)
    else:
        c_rate = TCanvas("c_"+Ctype+"_rate","c_"+Ctype+"_rate",1,1,1800,800)
    c_rate.SetGridx(True)
    c_rate.SetGridy(True)
    
    if pix:
        rate=TH1F(Ctype+"p_rate",Ctype+" : AlCaReco Pixel tracks rate",len(info_run_track),0,len(info_run_track))
        rate.GetYaxis().SetTitle("rate of alca pixel tracks (Hz)")
        ratePNG=TH1F(Ctype+"p_ratePNG",Ctype+" : AlCaReco Pixel tracks rate",len(info_run_track),0,len(info_run_track))
        ratePNG.GetYaxis().SetTitle("rate of alca pixel tracks (Hz)")
    else:
        rate=TH1F(Ctype+"_rate",Ctype+" : AlCaReco tracks rate",len(info_run_track),0,len(info_run_track))
        rate.GetYaxis().SetTitle("rate of alca tracks (Hz)")
        ratePNG=TH1F(Ctype+"_ratePNG",Ctype+" : AlCaReco tracks rate",len(info_run_track),0,len(info_run_track))
        ratePNG.GetYaxis().SetTitle("rate of alca tracks (Hz)")        
    rate.SetFillColor(kBlue+1)
    ratePNG.SetFillColor(kBlue+1)
    
    if pix:
        rate_processing=TH1F(Ctype+"p_rate_processing",Ctype+"p_rate_processing",len(info_run_track),0,len(info_run_track))
    else:
        rate_processing=TH1F(Ctype+"_rate_processing",Ctype+"_rate_processing",len(info_run_track),0,len(info_run_track))        
    rate_processing.SetLineColor(kGreen+1)
    rate_processing.SetFillColor(kGreen+1)

    
    #################
    #   FILL ALL    #
    #################    
    tickSpacing = round(len(info_run_track)/50., 0)
    tickCounter=-1
    for i in reversed(list(range(len(info_run_track)))):
        ibin = len(info_run_track)-i #careful, ibin is to plot the run numbers in the right order, while i and r are here to find the correct number of tracks associated to a run number
        cumulative_tracks+=info_run_track[i][1]
        if info_run_time[i][1] < 0:
            trend_processing.SetBinContent(ibin,info_run_track[i][1]);
            rate_processing.SetBinContent(ibin,float(info_run_track[i][1])/(abs(info_run_time[i][1]))); #The time is negative if the run is not fully processed yet
            cumul_processing.SetBinContent(ibin,cumulative_tracks);
        else:
            trend.SetBinContent(ibin,info_run_track[i][1]);
            trendPNG.SetBinContent(ibin,info_run_track[i][1]);
            rate.SetBinContent(ibin,float(info_run_track[i][1])/(info_run_time[i][1]));
            ratePNG.SetBinContent(ibin,float(info_run_track[i][1])/(info_run_time[i][1]));
            cumul.SetBinContent(ibin,cumulative_tracks);
            cumulPNG.SetBinContent(ibin,cumulative_tracks);
        if len(info_run_track) > 50:
            tickCounter += 1
            if tickCounter % tickSpacing == 0:
                trend.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
                trendPNG.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
                rate.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
                ratePNG.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
                cumul.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
                cumulPNG.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
            else:
                trend.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
                trendPNG.GetXaxis().SetBinLabel(ibin,"")
                rate.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
                ratePNG.GetXaxis().SetBinLabel(ibin,"")
                cumul.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
                cumulPNG.GetXaxis().SetBinLabel(ibin,"")
        else:
            trend.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
            trendPNG.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
            rate.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
            ratePNG.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
            cumul.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
            cumulPNG.GetXaxis().SetBinLabel(ibin,str(info_run_track[i][0]))
            

    ###################
    #  TREND DRAWING  #
    ###################            
    c_trend.cd()
    trendPNG.GetXaxis().SetRange(1, len(info_run_track))
    trendPNG.GetXaxis().LabelsOption("v")
    trendPNG.GetYaxis().SetRangeUser(0,max(trend.GetMaximum(),trend_processing.GetMaximum())*1.2)
    trendPNG.GetYaxis().SetTitleOffset(0.7)
    trendPNG.SetStats(0)
    trendPNG.Draw()
    trend_processing.Draw("same")
    c_trend.RedrawAxis()
    legend_info.Draw()
    Rleg.Draw()
    if pix:
        c_trend.SaveAs("Data/"+Ctype+"p.png")
    else:
        c_trend.SaveAs("Data/"+Ctype+".png")
    trend.GetXaxis().SetRange(1, len(info_run_track))
    trend.GetXaxis().LabelsOption("v")
    trend.GetYaxis().SetRangeUser(0,max(trend.GetMaximum(),trend_processing.GetMaximum())*1.2)
    trend.GetYaxis().SetTitleOffset(0.7)
    trend.SetStats(0)
    trend.Draw()
    trend_processing.Draw("same")
    c_trend.RedrawAxis()
    legend_info.Draw()
    Rleg.Draw()
    c_trend.Write()
    trend.Write()
    trend_processing.Write()

    ###################
    #  CUMUL DRAWING  #
    ###################
    c_cumul.cd()
    cumulPNG.GetXaxis().SetRange(1, len(info_run_track))
    cumulPNG.GetXaxis().LabelsOption("v")
    cumulPNG.GetYaxis().SetRangeUser(0,max(cumul.GetMaximum(),cumul_processing.GetMaximum())*1.2)
    cumulPNG.GetYaxis().SetTitleOffset(0.7)
    cumulPNG.SetStats(0)
    cumulPNG.Draw()
    cumul_processing.Draw("same")
    c_cumul.RedrawAxis()
    legend_info.Draw()
    Rleg.Draw()
    if pix:
        c_cumul.SaveAs("Data/"+Ctype+"p_cumul.png")
    else:
        c_cumul.SaveAs("Data/"+Ctype+"_cumul.png")
    cumul.GetXaxis().SetRange(1, len(info_run_track))
    cumul.GetXaxis().LabelsOption("v")
    cumul.GetYaxis().SetRangeUser(0,max(cumul.GetMaximum(),cumul_processing.GetMaximum())*1.2)
    cumul.GetYaxis().SetTitleOffset(0.7)
    cumul.SetStats(0)
    cumul.Draw()
    cumul_processing.Draw("same")
    c_cumul.RedrawAxis()
    legend_info.Draw()
    Rleg.Draw()
    c_cumul.Write()
    cumul.Write()
    cumul_processing.Write()

    ###################
    #   Rate DRAWING  #
    ###################
    c_rate.cd()
    ratePNG.GetXaxis().SetRange(1, len(info_run_track))
    ratePNG.GetXaxis().LabelsOption("v")
    ratePNG.GetYaxis().SetRangeUser(0,max(rate.GetMaximum(),rate_processing.GetMaximum())*1.2)
    ratePNG.GetYaxis().SetTitleOffset(0.7)
    ratePNG.SetStats(0)
    ratePNG.Draw()
    rate_processing.Draw("same")
    c_rate.RedrawAxis()
    legend_info.Draw()
    Rleg.Draw()
    if pix:
        c_rate.SaveAs("Data/"+Ctype+"p_rate.png")
    else:
        c_rate.SaveAs("Data/"+Ctype+"_rate.png")
    rate.GetXaxis().SetRange(1, len(info_run_track))
    rate.GetXaxis().LabelsOption("v")
    rate.GetYaxis().SetRangeUser(0,max(rate.GetMaximum(),rate_processing.GetMaximum())*1.2)
    rate.GetYaxis().SetTitleOffset(0.7)
    rate.SetStats(0)
    rate.Draw()
    rate_processing.Draw("same")
    c_rate.RedrawAxis()
    legend_info.Draw()
    Rleg.Draw()
    c_rate.Write()
    rate.Write()
    rate_processing.Write()
    

    
