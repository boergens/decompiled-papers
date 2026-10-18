function RP_wi = RESCOP_getConstrainedWeights(RP_wi)

% limit weights to >=0, normalize:
    RP_wi = exp(-RP_wi);RP_wi(RP_wi<10^-6)=0;RP_wi = RP_wi/sum(RP_wi);
    

end