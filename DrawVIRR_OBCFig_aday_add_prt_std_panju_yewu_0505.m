% Read grannul data of FY3C/VIRR and draw
% by XuHanlie 2014-4-11

clc; clear all; fclose all;close all
path='F:\data\FY\FY3C\VIRR\data\';
outpath='F:\data\FY\FY3C\VIRR\figure\';
% DATE='20131223';
sat='FY3C';
sensor='VIRR';

        bb_count=[];
        gain=[];
        lat=[];
        zen=[];
        prt1=[];
        prt2=[];
        std_BB=[];
        thre_l=[];
        thre_r=[];

for ifn=1:1
%     index=nam(ifn);
    index=20131220;
    numstr=sprintf('%04d',index);
    filedir1=strcat(path,numstr,'\');
    filedir_out=strcat(outpath,numstr,'\');
    filedir=strcat(path,numstr,'\*.hdf'); 
    filen=dir(filedir)
    n=size(filen,1);
    
    clear filename;
    for ij=145:145%循环读入当天的n个数据块
    filename=filen(ij).name;
    Time=filename(20:32);
    
    BB  =hdf5read([filedir1 filename],'/Calibration/Blackbody_View');
    SV  =hdf5read([filedir1 filename],'/Calibration/Space_View');
    PRT1=hdf5read([filedir1 filename],'/Calibration/PRT1_Count');
    PRT2=hdf5read([filedir1 filename],'/Calibration/PRT2_Count');
    AZ  =hdf5read([filedir1 filename],'/Geolocation/EVC_Azi_Zen');
    LL  =hdf5read([filedir1 filename],'/Geolocation/EVC_Lon_Lat');   
    IR_CAL_Offset=hdf5read([filedir1 filename],'/Calibration/Emissive_Radiance_Offsets')';
    IR_CAL_Scale =hdf5read([filedir1 filename],'/Calibration/Emissive_Radiance_Scales')';
    
    BB3=double(BB(:,:,3));
    SV3=double(SV(:,:,3));
%     LL=double(LL);
    AZ=double(AZ);
    PRT1=double(PRT1);
    PRT2=double(PRT2);
    
    BB3(BB3==0)=NaN;
    BB3(BB3<900)=NaN;
    SV3(SV3==0)=NaN;
    
    kk=find(LL(1,:)==LL(2,:));
    LL(1,kk)=NaN;
    LL(2,kk)=NaN;
    AZ(AZ==-32767)=NaN;
    PRT1(PRT1==65535 | PRT1==0)=NaN;
    PRT2(PRT2==65535 | PRT2==0)=NaN;
   
    BB_Ave=nanmean(BB3,1); %把BB和SV做平均
    SV_Ave=nanmean(SV3,1);
    PRT1_Ave=nanmean(PRT1,1);
    PRT2_Ave=nanmean(PRT2,1);
    PRT11_Ave=PRT1_Ave';
    PRT22_Ave=PRT2_Ave';
    clear PRT1_Ave PRT2_Ave;
    clear iij;
%     for iij=1:1800
%     PRT1_Ave(iij)=-6.273105 + 0.05394437*PRT11_Ave(iij) + (7.7615346e-7)*(PRT11_Ave(iij)^2)+ (6.936529e-10)*(PRT11_Ave(iij)^3);
%     PRT2_Ave(iij)=-6.5310216 + 0.05356502*PRT22_Ave(iij) + (1.3872694e-6)*(PRT22_Ave(iij)^2)+ (3.7068193e-10)*(PRT22_Ave(iij)^3);
%     end
    TimeH    =1:1800;
        y1(:,1) = BB_Ave(1,:);
        y1(:,2) = SV_Ave(1,:);
        
        y2(:,1) = IR_CAL_Scale(:,1)*1000;
        y2(:,2) = IR_CAL_Offset(:,1);
        
        y3(:,1) =  AZ(1,:)*0.01;
        y3(:,2) =  AZ(2,:)*0.01;
        
        y4(:,1) = LL(1,:);
        y4(:,2) = LL(2,:);
        
        y5(:,1) = PRT11_Ave(:);
        y5(:,2) = PRT22_Ave(:);
        
        y1=y1';
        y2=y2';
        y3=y3';
        y4=y4';
        y5=y5';
        
        %开始查找该数据块是否收到太阳污染
        %1、根据纬度和太阳天顶角确定危险区数据
         ll=find(y3(2,:)>75 & y3(2,:)<130& y4(2,:)>0);   %若数据在北半球
         ns=size(ll,2);
         if ns==0
            ll=find(y3(2,:)>90 & y3(2,:)<140 & y4(2,:)<0);   %若数据在南半球
            %ll=find(y3(2,:)>85 & y3(2,:)<125 & y4(2,:)<0);   %若数据在南半球
         end
         ns=size(ll,2);
         
         if ns>0   %若数据在大危险区当中，对数据块的BB进行统计，进一步确定污染的起始和结束位置
             %判断数据标准差是否存在剧烈变化由于数据变化厉害，先做个平滑
         windowSize = 101;  %101点滑动平均

            for j=1:1
              work(j,:)=smooth(y1(j,:),windowSize);
            end
          work(1,1:(windowSize-1)/2)=NaN; work(1,1800-(windowSize-1)/2+1:1800)=NaN;   %首尾数据定为缺测
%           work(work<930)=NaN;
          std_bb=nanstd(work);   %滑动平均后的标准差
          if (std_bb<0.4 & y4(2,:)>0) %若数据标准差较大，则认为存在污染，否则虽然在大污染区中，也不认为存在污染
              nz_l=0;nz_r=0;
          elseif (std_bb<0.7 & y4(2,:)<0) 
              nz_l=0;nz_r=0;
          else
         %2、在大范围内确定小范围（全数据污染，进污染区，出污染区） 
          %进一步通过太阳天顶角限制污染范围
            ll=find(y3(2,:)>85 & y3(2,:)<118 & y4(2,:)>0);   %若数据在北半球
            ns=size(ll,2);
            if ns==0
            ll=find(y3(2,:)>93 & y3(2,:)<123 & y4(2,:)<0);   %若数据在南半球
            %ll=find(y3(2,:)>85 & y3(2,:)<125 & y4(2,:)<0);   %若数据在南半球
            end
            a=min(ll);b=max(ll);  %根据纬度和南北半球，确定污染区大概范围
            %若纬度存在缺测值，可能会判断失误
            if (a>1)
                b=1800;
            end
            if(b<1800)
                a=1;
            end  
            
            if(a>1 | b<1800)  %对于入污染区或者出污染区的数据，用统计方法找出突变位置
            %将数据每间隔100个点求前后100个点的标准差
            for i=100:100:1700
                std_10(i/100,1)=nanstd(work(1,i-99:i+99));
                
            end
            
                
         
%           %对平滑后的数据，求201点滑动标准差
%             for i=101:1700
%                 std_10(i,1)=nanstd(work(1,i-100:i+100));   %对滑动平均后的数据进行每201点求标准差
%             end
%             std_10(1701:1800)=0;  %滑动前后的没数据的位置作为0
%             std_10(1:100)=0;       %滑动前后的没数据的位置作为0
%             std_10(std_10==0)=NaN;   %0值作为缺测
            %对上面的序列进行标准化处理
            std=((std_10-nanmean(std_10))/nanstd(std_10));  %将数据进行标准化
            std_1800(1:1800)=0;
            for i=100:100:1700
            std_1800(i)=std(i/100);
            end
            kk=find(abs(std_1800)>0.7);  %找到标准化之后大于0.8个标准差的数据
            end
           
           %确定污染区域的起止位置
             if (a==1 &b==1800)
                nz_l=1;nz_r=1800;  
             elseif (a==1 & b<1800)
                %nz_l=1;nz_r=max(kk)+15;  
                nz_l=1;nz_r=max(kk)+99;
             elseif (a>1 & b==1800);
                %nz_l=min(kk)-15;nz_r=1800;
                 nz_l=min(kk)-99;nz_r=1800;
             else
                nz_l=0;nz_r=0;
             end
             
          end
         
        y6(1,:)=y1(1,:);
        if(nz_l*nz_r)~=0
        y6(1,nz_l:nz_r)=NaN;
        end
        
        else  
           nz_l=0;nz_r=0;
           y6(1,:)=y1(1,:);
        end
%       
%         %画图
%         figure
%         subplot(2,2,1)
%         plot(1:1800,y1(1,:))
%         subplot(2,2,2)
%         plot(1:1800,y4(2,:))
%         subplot(2,2,3)
%         plot(1:1800,y6(1,:))
%         subplot(2,2,4)
%         plot(1:1800,y3(2,:))
%         
        
        thre_l=[thre_l nz_l];
        thre_r=[thre_r nz_r];
        
%         if std_bb>1.2
%             disp(ij)
%             figure
%             subplot(2,1,1)
%             plotyy(1:1800,work(1,:),1:1800,y3(2,:));
%             grid;
%             subplot(2,1,2)
%             plotyy(1:1800,work(1,:),1:1800,y4(2,:));
%             grid
%         end
%     end
        
        %bb_count=[bb_count work(1,:)];
        bb_count=[bb_count y1(1,:)];
        gain=[gain y2(1,:)];
        lat=[lat y4(2,:)];
        zen=[zen y3(2,:)];
        prt1=[prt1 y5(1,:)];
        prt2=[prt2 y5(2,:)];
%         std_BB=[std_BB std_bb];
%         std_BB=(std_BB-mean(std_BB))/std(std_BB);
        
       clear y1 y2 y3 y4 y5
       clearvars -except  n thre_l thre_r numstr sat sensor path outpaht index filedir1 filedir_out filedir filen n bb_count gain lat zen prt1 prt2 std_BB;
      
    close all
    end
 
end

% thre_l(thre_l==1|thre_l==0)=NaN;
% thre_r(thre_r==1800|thre_r==0)=NaN;
nn=size(bb_count,2);
n=size(thre_l,2);
thre_l(thre_l==0)=NaN;
thre_r(thre_r==0)=NaN;
for i=1:n
    thre_l(i)=(i-1)*1800+thre_l(i);
    thre_r(i)=(i-1)*1800+thre_r(i);
%     latitude_1(i)=latitude(thre_l(i));
    if (isnan(thre_l(i))==0 )
        if(mod(thre_l(i),10)>1)
    sza_1(i)=zen(thre_l(i));
        end
    end
    if (isnan(thre_r(i))==0)
        if(mod(thre_r(i),10)>1)
         sza_2(i)=zen(thre_r(i));
        end
    
    end
    if (isnan(thre_l(i))==0 )
        if(mod(thre_l(i),10)>1)
    lat_1(i)=lat(thre_l(i));
        end
    end
    if (isnan(thre_r(i))==0)
        if(mod(thre_r(i),10)>1)
         lat_2(i)=lat(thre_r(i));
        end
    
    end
    
end
% ii=find(sza_1>0);
% sza_11=sza_1(ii);lat_11=lat_1(ii);
% zen_1=max(sza_11);zen_11=mean(sza_11);
% lati_1=max(lat_11);lati_11=mean(lat_11);
% clear ii;
% 
% ii=find(sza_2>0);
% sza_22=sza_2(ii);lat_22=lat_2(ii);
% zen_2=min(sza_22);zen_22=mean(sza_22);
% lati_2=max(lat_22);lati_22=mean(lat_22);
y1(1:n)=958;
y2(1:n)=958;
subplot(2,1,1)
for i=1:n
%     if (mod(thre_l(i),10)==1)
line([thre_l(i),thre_r(i)],[y1(i),y2(i)],'color','r')
    
% line([thre_r(i),thre_r(i)],[y1(i),y2(i)],'color','r')
if(isnan(thre_l(i))==0 & isnan(thre_r(i))==0)
%   bb_count(thre_l(i):thre_r(i))=NaN;
end
end
% y1(1:n)=900;
% y2(1:n)=1000;
% for i=1:n
% line([thre_l(i),thre_l(i)],[y1(i),y2(i)],'color','r')
% line([thre_r(i),thre_r(i)],[y1(i),y2(i)],'color','r')
% end
 hold on
[AX,H1,H2] =plotyy(1:n*1800,bb_count,1:n*1800,zen)

%         set(AX(1),'XColor','k','YColor','b'); 
%         set(AX(2),'XColor','k','YColor','r');  %右纵坐标轴颜色
        set(AX(1),'ylim',[940,970],'YTick',940:5:970)
        set(AX(2),'ylim',[0,180],'YTick',0:30:180)
        set(AX(1),'xlim',[0,nn],'YTick',0:100000:nn)
        set(AX(2),'xlim',[0,nn],'YTick',0:100000:nn)
        set(get(AX(1),'Ylabel'),'String','BB Counts','FontSize',10) 
        set(get(AX(2),'Ylabel'),'String','Solar Zenith Angle','FontSize',10) 
        
%         set(H1(1),'LineStyle','-','color','b','Markersize',2)
%         set(H2(1),'LineStyle','-','color','r','Markersize',1.5)
       
%         legend('\fontsize{10}BB Count','\fontsize{10}SZA',0);
        legend('boxoff'); %去掉图例边框
%         set(AX(1),'Ycolor','g','Ylim',[BMIN4 BMAX4],'Ytick',BMIN4:20:BMAX4); %设置y轴间隔 ,'ytick',BMIN4:0.5:BMAX4
%         set(AX(2),'Ycolor','m','Ylim',[TMIN   TMAX],'Ytick',TMIN :1:TMAX)
%         set(AX,'xlim',THrange,'XTicklabel','') % 设置x轴范围
        set(gca, 'Fontname', 'Arial','YMinorTick','on','XMinorTick','on')
        grid;
        
        subplot(2,1,2)
        for i=1:n
%     if (mod(thre_l(i),10)==1)
line([thre_l(i),thre_r(i)],[y1(i),y2(i)],'color','r')
    
% line([thre_r(i),thre_r(i)],[y1(i),y2(i)],'color','r')
if(isnan(thre_l(i))==0 & isnan(thre_r(i))==0)
  bb_count(thre_l(i):thre_r(i))=NaN;
end
end
% y1(1:n)=900;
% y2(1:n)=1000;
% for i=1:n
% line([thre_l(i),thre_l(i)],[y1(i),y2(i)],'color','r')
% line([thre_r(i),thre_r(i)],[y1(i),y2(i)],'color','r')
% end
 hold on
[AX,H1,H2] =plotyy(1:n*1800,bb_count,1:n*1800,zen)

%         set(AX(1),'XColor','k','YColor','b'); 
%         set(AX(2),'XColor','k','YColor','r');  %右纵坐标轴颜色
        set(AX(1),'ylim',[940,970],'YTick',940:5:970)
        set(AX(2),'ylim',[0,180],'YTick',0:30:180)
        set(AX(1),'xlim',[0,nn],'YTick',0:100000:nn)
        set(AX(2),'xlim',[0,nn],'YTick',0:100000:nn)
        set(get(AX(1),'Ylabel'),'String','BB Counts','FontSize',10) 
        set(get(AX(2),'Ylabel'),'String','Solar Zenith Angle','FontSize',10) 
        
%         set(H1(1),'LineStyle','-','color','b','Markersize',2)
%         set(H2(1),'LineStyle','-','color','r','Markersize',1.5)
       
%         legend('\fontsize{10}BB Count','\fontsize{10}SZA',0);
        legend('boxoff'); %去掉图例边框
%         set(AX(1),'Ycolor','g','Ylim',[BMIN4 BMAX4],'Ytick',BMIN4:20:BMAX4); %设置y轴间隔 ,'ytick',BMIN4:0.5:BMAX4
%         set(AX(2),'Ycolor','m','Ylim',[TMIN   TMAX],'Ytick',TMIN :1:TMAX)
%         set(AX,'xlim',THrange,'XTicklabel','') % 设置x轴范围
        set(gca, 'Fontname', 'Arial','YMinorTick','on','XMinorTick','on')
        grid;







    return