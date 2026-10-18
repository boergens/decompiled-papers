function [RP_logLikl,RP_histPredout] = RESCOP_getLogLikelihoodFromWeights_v2(RP_w,RP_priorCiNT,RP_histMeasStar,RP_logCum)

    % limit weights to >=0, normalize:
    RP_w = RESCOP_getConstrainedWeights(RP_w);
    
    RP_histPred_unnorm = squeeze(sum(repmat(RP_w,[1,size(RP_priorCiNT,2),size(RP_priorCiNT,3)]).*RP_priorCiNT,1));
    RP_normalization = repmat(sum(RP_histMeasStar(2:end,:),1),[size(RP_priorCiNT,2) 1])./...
        repmat(1-sum(repmat(RP_w,[1 size(RP_priorCiNT,3)]).*squeeze(RP_priorCiNT(:,0+1,:)),1),[size(RP_priorCiNT,2) 1]);
    RP_histPred = RP_histPred_unnorm.*RP_normalization;

    RP_logLikl_term1 = -RP_histPred(2:end,2:end);
    RP_logLikl_term3 = RP_logCum(RP_histMeasStar(2:end,2:end)+1);
    RP_logLikl_term2a = RP_histMeasStar(2:end,2:end);
    RP_logLikl_term2b = RP_histPred(2:end,2:end);
    RP_logLikl_term2 = RP_logLikl_term2a.*log(RP_logLikl_term2b);
    RP_logLikl_term2(logical((RP_logLikl_term2a==0).*(RP_logLikl_term2b==0))) = 0;
    
    RP_logLikl_mx = RP_logLikl_term1 + RP_logLikl_term2 - RP_logLikl_term3;
%     RP_logLikl_mx = -RP_histPred(2:end,2:end) + RP_histMeasStar(2:end,2:end).*log(RP_histPred(2:end,2:end)) - RP_logCum(RP_histMeasStar(2:end,2:end)+1);
    RP_logLikl = -sum(sum(RP_logLikl_mx(2:end,2:end))); % -logL for fminsearch

    % log likelihood:
% sum(-histPred + histmeasStar*log(histPred)-(sumi=1..histmeasStar(logi)))_T=1..N,N

    if nargout>1
        RP_histPredout = RP_histPred;
    end
end