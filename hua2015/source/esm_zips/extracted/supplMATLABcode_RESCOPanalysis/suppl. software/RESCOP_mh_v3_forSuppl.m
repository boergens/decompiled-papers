%% Fit vote histograms (for Hua Laserstein Helmstaedter)
% mh@brain.mpg.de



%% e1088

load(fullfile('C:\Users\mh\Documents\_mhlab\publications\2014 stainingPaper\2014_12_19_Traceability\e1088_data_fromHD',...
    'e1088_skeletonSnapshot_2008-12-02_skeletons_justSkeletons_edgeVotes_allSets_voteHistogram.mat'));
RP_histMeas = kl_voteHistogram; % zeros or no zeros doesn't matter since not used. However: always T+1, N+1, i+1 as entry indices
RP_histMeasStar = round(RP_histMeas./repmat([0:size(RP_histMeas,1)-1]',[1 size(RP_histMeas,2)]));
RP_Nmax = size(RP_histMeas,2)-1
RP_imax=80
RP_rhos = RESCOP_priorBasisPoints(RP_imax);
RP_priorCiNT = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax);

RP_w_init = repmat(1,[RP_imax+1,1]);
RP_logCum = [0 cumsum(log([1:max(RP_histMeasStar(~isinf(RP_histMeasStar)))]))];   % indexed +1; factorial 0 = 1

options = optimset;    
options.MaxFunEvals = 10^6
options.MaxIter = 10^6
options.TolFun = 10^(-7)

[RP_params_min,RP_min,exitflag,output] = ...
        fminsearch(@(RP_w) RESCOP_getLogLikelihoodFromWeights_v2(RP_w,RP_priorCiNT,RP_histMeasStar,RP_logCum),...
        RP_w_init,options)

RP_w_fitResultConstrained = RESCOP_getConstrainedWeights(RP_params_min);
[RP_priorx,RP_priory] = RESCOP_getPrior(RP_rhos,RP_params_min);
figure,subplot(1,2,1),plot(RP_priorx,RP_priory);subplot(1,2,2),plot(RP_priorx,RP_priory); set(gca,'YScal','log','YLim',[10^-2 10^3]);

[RP_logLikl,RP_histPredFinal] = RESCOP_getLogLikelihoodFromWeights_v2(RP_params_min,RP_priorCiNT,RP_histMeasStar,RP_logCum);
max(RP_histMeasStar(:))
max(RP_histPredFinal(:))
figure,subplot(1,2,1),image(log(RP_histPredFinal),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);
subplot(1,2,2),image(log(RP_histMeasStar),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);

% calculate error rate prediction
icmin = find(RP_rhos>=0.5,1)
RP_Nmax_forExtrap = 50
RP_priorCiNT_05 = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax_forExtrap,icmin);
RP_priorCiNT_05_NT = squeeze(sum(repmat(RP_w_fitResultConstrained,[1,size(RP_priorCiNT_05,2),size(RP_priorCiNT_05,3)]).*RP_priorCiNT_05,1));
RP_priorCiNT_0_extrap = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax_forExtrap,1);
RP_priorCiNT_0_NT_extrap = squeeze(sum(repmat(RP_w_fitResultConstrained,[1,size(RP_priorCiNT_0_extrap,2),size(RP_priorCiNT_0_extrap,3)]).*RP_priorCiNT_0_extrap,1));

RP_pkeep = RP_priorCiNT_05_NT./RP_priorCiNT_0_NT_extrap;
RP_perrNT = min(RP_pkeep,1-RP_pkeep);
RP_p_errN = nansum(RP_perrNT.*RP_priorCiNT_0_NT_extrap,1)

RP_rp = 1.2 %µm 
RP_errDist = RP_rp./RP_p_errN;
figure,plot(RP_errDist(2:end));set(gca,'YScal','log');

save(fullfile('C:\Users\mh\Documents\_mhlab\publications\2014 stainingPaper\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','YH_MH_old_e1088Data_refit_mh_v2.mat'));

%% YH DATA

% load(fullfile('X:\Personal\mh\_mhlab\publications\2014 stainingPaper\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','YH_MH_voteHist.mat'),'vote_matrix','correction_matrix','D');
load(fullfile('C:\Users\mh\Documents\_mhlab\publications\2014 stainingPaper\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','YH_MH_voteHist.mat'),'vote_matrix','correction_matrix','D');
% note: correction mx is wrong
RP_vote_matrix_YH = repmat(0,size(vote_matrix)+1);
RP_vote_matrix_YH(2:end,2:end) = vote_matrix;
RP_histMeas = RP_vote_matrix_YH; % zeros or no zeros doesn't matter since not used. However: always T+1, N+1, i+1 as entry indices
RP_histMeasStar = round(RP_histMeas./repmat([0:size(RP_histMeas,1)-1]',[1 size(RP_histMeas,2)]));

RP_Nmax = size(RP_histMeas,2)-1
RP_imax=80
RP_rhos = RESCOP_priorBasisPoints(RP_imax);
RP_priorCiNT = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax);

RP_w_init = repmat(1,[RP_imax+1,1])
RP_logCum = [0 cumsum(log([1:max(RP_histMeasStar(~isinf(RP_histMeasStar)))]))];   % indexed +1; factorial 0 = 1

options = optimset;    
options.MaxFunEvals = 10^6;
options.MaxIter = 10^6;
options.TolFun = 10^(-7);

[RP_params_min,RP_min,exitflag,output] = ...
        fminsearch(@(RP_w) RESCOP_getLogLikelihoodFromWeights_v2(RP_w,RP_priorCiNT,RP_histMeasStar,RP_logCum),...
        RP_w_init,options)

RP_w_fitResultConstrained = RESCOP_getConstrainedWeights(RP_params_min);
[RP_priorx,RP_priory] = RESCOP_getPrior(RP_rhos,RP_params_min);
figure,subplot(1,2,1),plot(RP_priorx,RP_priory);subplot(1,2,2),plot(RP_priorx,RP_priory); set(gca,'YScal','log','YLim',[10^-2 10^3]);

[RP_logLikl,RP_histPredFinal] = RESCOP_getLogLikelihoodFromWeights_v2(RP_params_min,RP_priorCiNT,RP_histMeasStar,RP_logCum);
max(RP_histMeasStar(:))
max(RP_histPredFinal(:))
figure,subplot(1,2,1),image(log(RP_histPredFinal),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);
subplot(1,2,2),image(log(RP_histMeasStar),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);

% calculate error rate prediction
icmin = find(RP_rhos>=0.5,1)
RP_Nmax_forExtrap = 50
RP_priorCiNT_05 = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax_forExtrap,icmin);
RP_priorCiNT_05_NT = squeeze(sum(repmat(RP_w_fitResultConstrained,[1,size(RP_priorCiNT_05,2),size(RP_priorCiNT_05,3)]).*RP_priorCiNT_05,1));
RP_priorCiNT_0_extrap = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax_forExtrap,1);
RP_priorCiNT_0_NT_extrap = squeeze(sum(repmat(RP_w_fitResultConstrained,[1,size(RP_priorCiNT_0_extrap,2),size(RP_priorCiNT_0_extrap,3)]).*RP_priorCiNT_0_extrap,1));

RP_pkeep = RP_priorCiNT_05_NT./RP_priorCiNT_0_NT_extrap;
RP_perrNT = min(RP_pkeep,1-RP_pkeep);
RP_p_errN = nansum(RP_perrNT.*RP_priorCiNT_0_NT_extrap,1)

RP_rp = 1.2 %µm 
RP_errDist = RP_rp./RP_p_errN;
figure,plot(RP_errDist(2:end));set(gca,'YScal','log');

save(fullfile('C:\Users\mh\Documents\_mhlab\publications\2014 stainingPaper\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','YH_MH_traceabilityData_fit_mh_v2.mat'));

%% L4 cortex data KMB

% load(fullfile('X:\Personal\mh\_mhlab\publications\2014 stainingPaper\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','YH_MH_voteHist.mat'),'vote_matrix','correction_matrix','D');
load(fullfile('C:\Users\mh\Documents\_mhlab\publications\2014 L4cortex\2015_01_03_traceability','vote_matrix_for_mh_2014-12-30.mat'));
% note: correction mx is wrong
RP_vote_matrix_KMB = repmat(0,size(vote_matrix)+1);
RP_vote_matrix_KMB(2:end,2:end) = vote_matrix;
RP_histMeas = RP_vote_matrix_KMB; % zeros or no zeros doesn't matter since not used. However: always T+1, N+1, i+1 as entry indices
RP_histMeasStar = round(RP_histMeas./repmat([0:size(RP_histMeas,1)-1]',[1 size(RP_histMeas,2)]));

RP_Nmax = size(RP_histMeas,2)-1
RP_imax=80
RP_rhos = RESCOP_priorBasisPoints(RP_imax);
RP_priorCiNT = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax);

RP_w_init = repmat(1,[RP_imax+1,1])
RP_logCum = [0 cumsum(log([1:max(RP_histMeasStar(~isinf(RP_histMeasStar)))]))];   % indexed +1; factorial 0 = 1

options = optimset;    
options.MaxFunEvals = 10^6;
options.MaxIter = 10^6;
options.TolFun = 10^(-7);

[RP_params_min,RP_min,exitflag,output] = ...
        fminsearch(@(RP_w) RESCOP_getLogLikelihoodFromWeights_v2(RP_w,RP_priorCiNT,RP_histMeasStar,RP_logCum),...
        RP_w_init,options)

RP_w_fitResultConstrained = RESCOP_getConstrainedWeights(RP_params_min);
[RP_priorx,RP_priory] = RESCOP_getPrior(RP_rhos,RP_params_min);
figure,subplot(1,2,1),plot(RP_priorx,RP_priory);subplot(1,2,2),plot(RP_priorx,RP_priory); set(gca,'YScal','log','YLim',[10^-2 10^3]);

[RP_logLikl,RP_histPredFinal] = RESCOP_getLogLikelihoodFromWeights_v2(RP_params_min,RP_priorCiNT,RP_histMeasStar,RP_logCum);
max(RP_histMeasStar(:))
max(RP_histPredFinal(:))
figure,subplot(1,2,1),image(log(RP_histPredFinal),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);
subplot(1,2,2),image(log(RP_histMeasStar),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);

% calculate error rate prediction
icmin = find(RP_rhos>=0.5,1)
RP_Nmax_forExtrap = 50
RP_priorCiNT_05 = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax_forExtrap,icmin);
RP_priorCiNT_05_NT = squeeze(sum(repmat(RP_w_fitResultConstrained,[1,size(RP_priorCiNT_05,2),size(RP_priorCiNT_05,3)]).*RP_priorCiNT_05,1));
RP_priorCiNT_0_extrap = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax_forExtrap,1);
RP_priorCiNT_0_NT_extrap = squeeze(sum(repmat(RP_w_fitResultConstrained,[1,size(RP_priorCiNT_0_extrap,2),size(RP_priorCiNT_0_extrap,3)]).*RP_priorCiNT_0_extrap,1));

RP_pkeep = RP_priorCiNT_05_NT./RP_priorCiNT_0_NT_extrap;
RP_perrNT = min(RP_pkeep,1-RP_pkeep);
RP_p_errN = nansum(RP_perrNT.*RP_priorCiNT_0_NT_extrap,1)

RP_rp = 2*0.4 %µm 
RP_errDist = RP_rp./RP_p_errN;
figure,plot(RP_errDist(2:end));set(gca,'YScal','log');

save(fullfile('C:\Users\mh\Documents\_mhlab\publications\2014 stainingPaper\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','KMB_MH_traceabilityData_fit_mh_v2.mat'));


%% just plot results together

close all; clear all;
% RP_path = 'C:\Users\mh\Documents\_mhlab\publications\2014 stainingPaper\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP'
RP_path = 'X:\Personal\mh\_mhlab\publications\2014 stainingPaper\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP'

load(fullfile(RP_path,'YH_MH_old_e1088Data_refit_mh_v2.mat'));
figure,subplot(1,2,1),plot(RP_priorx,RP_priory);set(gca,'XLim',[-0.1 1.1]);
subplot(1,2,2),plot(RP_priorx,max(RP_priory,10^-2)); set(gca,'YScal','log','YLim',[10^-1 10^3]);set(gca,'XLim',[-0.1 1.1]);
title('e1088');
figure,subplot(1,2,1),image(log(RP_histPredFinal),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);
subplot(1,2,2),image(log(RP_histMeasStar),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);
title('e1088');
RP_rp = 2*0.6 %µm 
RP_errDist = RP_rp./RP_p_errN;
figure(99),plot(RP_errDist(2:end),'b');set(gca,'YScal','log');hold on

load(fullfile(RP_path,'YH_MH_traceabilityData_fit_mh_v2.mat'));
figure,subplot(1,2,1),plot(RP_priorx,RP_priory);set(gca,'XLim',[-0.1 1.1]);
subplot(1,2,2),plot(RP_priorx,max(RP_priory,10^-2)); set(gca,'YScal','log','YLim',[10^-1 10^3]);set(gca,'XLim',[-0.1 1.1]);
title('YH');
figure,subplot(1,2,1),image(log(RP_histPredFinal),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);
subplot(1,2,2),image(log(RP_histMeasStar),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);
title('YH');
RP_rp = 2*0.4 %µm 
RP_errDist = RP_rp./RP_p_errN;
figure(99),plot(RP_errDist(2:end),'r');set(gca,'YScal','log');

load(fullfile(RP_path,'KMB_MH_traceabilityData_fit_mh_v2.mat'));
figure,subplot(1,2,1),plot(RP_priorx,RP_priory);set(gca,'XLim',[-0.1 1.1]);
subplot(1,2,2),plot(RP_priorx,max(RP_priory,10^-2)); set(gca,'YScal','log','YLim',[10^-1 10^3]);set(gca,'XLim',[-0.1 1.1]);
title('KMB L4');
figure,subplot(1,2,1),image(log(RP_histPredFinal),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);
subplot(1,2,2),image(log(RP_histMeasStar),'CDataMapping','scaled');set(gca,'CLim',[0 log(max(RP_histMeasStar(:)))]);
title('KMB L4');
RP_rp = 2*0.4 %µm 
RP_errDist = RP_rp./RP_p_errN;
figure(99),plot(RP_errDist(2:end),'g');set(gca,'YScal','log');


%% focused reannotation

% load alternatively:
clear all, close all
%  load(fullfile('E:\mh_tempwork\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','YH_MH_old_e1088Data_refit_mh_v2.mat'));
% load(fullfile('E:\mh_tempwork\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','YH_MH_traceabilityData_fit_mh_v2.mat'));
load(fullfile('E:\mh_tempwork\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','KMB_MH_traceabilityData_fit_mh_v2.mat'));


% calculate error rate prediction for sufficiently large N. Takes ~30
% minutes
icmin = find(RP_rhos>=0.5,1)
RP_Nmax_forExtrap = 500
RP_nckSwitch=0; % nchoosek factor not needed since normalized in later step
RP_priorCiNT_05 = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax_forExtrap,icmin,RP_nckSwitch);
RP_priorCiNT_05_NT = squeeze(sum(repmat(RP_w_fitResultConstrained,[1,size(RP_priorCiNT_05,2),size(RP_priorCiNT_05,3)]).*RP_priorCiNT_05,1));
RP_priorCiNT_0_extrap = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax_forExtrap,1,RP_nckSwitch);
RP_priorCiNT_0_NT_extrap = squeeze(sum(repmat(RP_w_fitResultConstrained,[1,size(RP_priorCiNT_0_extrap,2),size(RP_priorCiNT_0_extrap,3)]).*RP_priorCiNT_0_extrap,1));

RP_pkeep = RP_priorCiNT_05_NT./RP_priorCiNT_0_NT_extrap;
RP_perrNT = min(RP_pkeep,1-RP_pkeep);
RP_p_errN = nansum(RP_perrNT.*RP_priorCiNT_0_NT_extrap,1)
RP_toshow = RP_perrNT;
RP_toshow = real(log10(RP_toshow));
% RP_toshow(RP_toshow<-5)=nan;
figure,image(RP_toshow,'CDataMapping','scaled');set(gca,'CLim',[-5 0]);
set(gca,'XLim',[1 26],'YLim',[1 26]);
daspect([1 1 1])

% sample pes
[RP_priorx,RP_priory] = RESCOP_getPrior(RP_rhos,RP_params_min);
RP_xinterp = linspace(0,1,10^5);
RP_prior_interp = interp1(RP_priorx,RP_priory,RP_xinterp);
figure,plot(RP_xinterp,RP_prior_interp);set(gca,'XLim',[-0.1 1.1]);
RP_priorCum = cumsum(RP_prior_interp)/sum(RP_prior_interp);
figure,plot(RP_xinterp,RP_priorCum);set(gca,'XLim',[-0.1 1.1],'YLim',[-0.1 1.1]);

RP_priorExcl = find(diff(RP_priorCum)==0)+1;
RP_priorCum_squeezed = RP_priorCum(setdiff(1:length(RP_priorCum),RP_priorExcl));
RP_priorCum_squeezed_x = RP_xinterp(setdiff(1:length(RP_priorCum),RP_priorExcl));
figure,plot(RP_priorCum_squeezed_x,RP_priorCum_squeezed);
figure,plot(RP_priorCum_squeezed,RP_priorCum_squeezed_x);

% draw pes, coin toss
RP_npeDraws = 1000;
RP_nmaxToss = 500;
RP_randoms = rand(RP_npeDraws,RP_nmaxToss);
RP_sample = rand(RP_npeDraws,1);
RP_peSample = interp1(RP_priorCum_squeezed,RP_priorCum_squeezed_x,RP_sample,'nearest');
RP_sampleMx = repmat(RP_peSample,[1 RP_nmaxToss]);
figure,hist(RP_peSample,linspace(0,1,1000));

RP_votes = RP_randoms<=RP_sampleMx;
RP_votesCum = cumsum(RP_votes,2);
RP_N = repmat(1:RP_nmaxToss,[RP_npeDraws,1]);

RP_votesTest = RP_votesCum(:,1:RP_nmaxToss);
RP_Ntest = RP_N(:,1:RP_nmaxToss);
RP_pos_ind = sub2ind(size(RP_perrNT),RP_votesTest(:)+1,RP_Ntest(:)+1);
RP_perrDraws = reshape(RP_perrNT(RP_pos_ind),size(RP_votesTest,1),size(RP_votesTest,2));
% numerical bleed-over: some entries almost zero but neg.


RP_corrlength = 1.2 %µm
RP_setLengthGoalList = 10.^[2 3 5 7]
RP_focusedAnnotationPred=[];

for RP_lgc=1:length(RP_setLengthGoalList)
    RP_setLengthGoal = RP_setLengthGoalList(RP_lgc) %µm
    RP_setErrGoal = RP_corrlength/RP_setLengthGoal
    
    RP_perrContinued = RP_perrDraws>RP_setErrGoal;
    RP_perrStopped = RP_perrDraws<=RP_setErrGoal;
    RP_firstAchieved=[];
    for i=1:size(RP_perrStopped,1)
        RP_thisfirst = find(RP_perrStopped(i,:)>0,1);
        if ~isempty(RP_thisfirst)
            RP_firstAchieved(i)=max(RP_thisfirst-1,1);
        else
            RP_firstAchieved(i) = nan;
        end
    end
    RP_uncorravg = (nansum(RP_firstAchieved) + length(find(isnan(RP_firstAchieved)))*size(RP_perrStopped,2))/size(RP_perrStopped,1)
    RP_remainingError = mean(RP_perrDraws(isnan(RP_firstAchieved),end))* length(find(isnan(RP_firstAchieved))) / size(RP_perrStopped,1)
    RP_corrErrGoal = 1/(RP_setErrGoal+RP_remainingError)
    RP_avgRedFocused = RP_uncorravg
    
    RP_focusedAnnotationPred(RP_lgc,1:6) = [size(RP_perrStopped,1), length(find(isnan(RP_firstAchieved))), RP_uncorravg, RP_avgRedFocused, RP_setLengthGoal, RP_corrErrGoal];
    if RP_focusedAnnotationPred(RP_lgc,2)==0 % no correction necessary
        RP_focusedAnnotationPred(RP_lgc,7) = RP_setLengthGoal;
    else
        RP_focusedAnnotationPred(RP_lgc,7) = RP_corrErrGoal;
    end
end

figure,plot(RP_focusedAnnotationPred(:,4),RP_focusedAnnotationPred(:,7),'--');set(gca,'YScal','log');
set(gca,'XLim',[0 50],'YLim',[10^0 10^8])

% save(fullfile('E:\mh_tempwork\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','YH_MH_old_e1088Data_refit_mh_v2_FocAnn.mat'));
% save(fullfile('E:\mh_tempwork\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','YH_MH_traceabilityData_fit_mh_v2_FocAnn.mat'));
% save(fullfile('E:\mh_tempwork\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP','KMB_MH_traceabilityData_fit_mh_v2_FocAnn.mat'));

%% plot results together into non-focused plot

hold on
RP_path = 'X:\Personal\mh\_mhlab\publications\2014 stainingPaper\2014_12_19_Traceability\Traceability_Yunfeng\RESCOP'
load(fullfile(RP_path,'YH_MH_old_e1088Data_refit_mh_v2_FocAnn.mat'));
plot(RP_focusedAnnotationPred(:,4),RP_focusedAnnotationPred(:,7),'--b');
load(fullfile(RP_path,'YH_MH_traceabilityData_fit_mh_v2_FocAnn.mat'));
plot(RP_focusedAnnotationPred(:,4),RP_focusedAnnotationPred(:,7),'--r');
load(fullfile(RP_path,'KMB_MH_traceabilityData_fit_mh_v2_FocAnn.mat'));
plot(RP_focusedAnnotationPred(:,4),RP_focusedAnnotationPred(:,7),'--g');

title('e1008 (b); YH (r); KMB (g) (--: focused annotation)');
xlabel('# annotators');
ylabel('avg inter-error distance (µm)');

















