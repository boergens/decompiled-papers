function [RP_priorx,RP_priory] = RESCOP_getPrior(RP_rhos,RP_wi)

    % limit weights to >=0, normalize:
    RP_wi = RESCOP_getConstrainedWeights(RP_wi);
    
    
    % create basis functions:
    RP_bases = repmat(0,length(RP_wi),length(RP_rhos));
    RP_basisNorms = [diff(RP_rhos(1:2))/2, (RP_rhos(3:end) - RP_rhos(1:end-2))/2, diff(RP_rhos(end-1:end))/2];
    RP_bases(1,1:2) = [1 0]/RP_basisNorms(1);
    RP_bases(end,end-1:end) = [0 1]/RP_basisNorms(end);
    for i=2:length(RP_rhos)-1
        RP_bases(i,i-1:i+1)= [0 1 0]/RP_basisNorms(i);
    end
    RP_basesW = RP_bases.*repmat(RP_wi,[1 size(RP_bases,2)]);
    
    RP_priorx = RP_rhos;
    RP_priory = sum(RP_basesW,1);
end