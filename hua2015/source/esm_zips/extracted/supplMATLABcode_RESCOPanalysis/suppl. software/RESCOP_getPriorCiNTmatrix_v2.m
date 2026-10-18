function RP_priorCiNT = RESCOP_getPriorCiNTmatrix_v2(RP_rhos,RP_Nmax,icmin,RP_nck_switch)
    
    % explicit integration via beta fctn; 
    % allow limited integration (for pkeep, then set icmin to rho==0.5;
    % works only for exists rho exactly 0.5
    % nchoosek factor can be left out if normalized later anyway
    % (RP_nck_switch)

    % rising edge: integrand = p^T*(1-p)^(N-T)*a(p-rho_i-1) =
    % a*p^(T+1)(1-p)^(N-T) - a(rho_i-1)*p^T*(1-p)^(N-T) from rho_i-1:rho_i with
    % a=peaki/(rho_i-rho_i-1) and peaki = 1/areai and areai =
    % (rho_i+1-rho_i-1)/2
    % falling edge: integrand = p^T*(1-p)^(N-T)*b(p-rho_i+1) =
    % b*p^(T+1)(1-p)^(N-T) - b(rho_i+1)*p^T*(1-p)^(N-T) from rho_i:rho_i+1 with
    % b=-peaki/(rho_i+1-rho_i) and peaki = 1/areai and areai =
    % (rho_i+1-rho_i-1)/2
    
    RP_priorCiNT=repmat(0,[length(RP_rhos),RP_Nmax+1,RP_Nmax+1]);
    icmax = length(RP_rhos);
    if nargin<3
        icmin=1
    end 
    if nargin<4
        RP_nck_switch=1;
    end
    RP_prefactor = repmat(1,RP_Nmax+1,RP_Nmax+1);
    if RP_nck_switch
        for N=1:RP_Nmax
            for T=0:N        
                RP_prefactor(T+1,N+1) = nchoosek(N,T);
            end
        end
    end
    for ic = icmin:icmax  % matlab index, ic = i+1 wrt i in formulas
        fprintf('ic: %d ; ',ic);
        for N=1:RP_Nmax
            for T=0:N
                if ic==icmin
                    RP_peak = 2/(RP_rhos(ic+1)-0.5);
                elseif ic==icmax
                    RP_peak = 2/(1-RP_rhos(ic-1));
                else
                    RP_peak = 2/(RP_rhos(ic+1)-RP_rhos(ic-1));
                end
                RP_int11 = betainc_unnorm(RP_rhos(ic),T+2,N-T+1);
                RP_int21 = betainc_unnorm(RP_rhos(ic),T+1,N-T+1);                
                if ic>icmin
                    RP_int12 = betainc_unnorm(RP_rhos(ic-1),T+2,N-T+1);
                    RP_int22 = betainc_unnorm(RP_rhos(ic-1),T+1,N-T+1);
                    RP_int1 = RP_int11 - RP_int12;
                    RP_int2 = RP_int21 - RP_int22;
                    RP_a = RP_peak/(RP_rhos(ic)-RP_rhos(ic-1));
                    RP_integral1 = RP_a*RP_int1 - RP_a*RP_rhos(ic-1)*RP_int2;
                else
                    RP_integral1 = 0;
                end
                if ic<icmax
                    RP_int13 = betainc_unnorm(RP_rhos(ic+1),T+2,N-T+1);
                    RP_int23 = betainc_unnorm(RP_rhos(ic+1),T+1,N-T+1);
                    RP_int3 = RP_int13 - RP_int11;
                    RP_int4 = RP_int23 - RP_int21;
                    RP_b = -RP_peak/(RP_rhos(ic+1)-RP_rhos(ic));
                    RP_integral2 = RP_b*RP_int3 - RP_b*RP_rhos(ic+1)*RP_int4;
                else
                    RP_integral2 = 0;
                end
                RP_priorCiNT(ic,T+1,N+1)= RP_prefactor(T+1,N+1)*(RP_integral1 + RP_integral2);
            end
        end
    end
    
end