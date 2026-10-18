function RP_priorBasisPoints = RESCOP_priorBasisPoints(imax)
% reimplemented 12/2014, mh@brain.mpg.de
    if nargin<1
        imax=80;
    end
        
    RP_priorBasisPoints = [2*([0:imax/2-1]/imax).^2, (1-2*(1-([imax/2:imax]/imax)).^2)];
%     figure,plot(RP_priorBasisPoints,1,'x')

end