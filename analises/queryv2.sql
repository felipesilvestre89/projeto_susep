select codigosusep
, case when substring(codigosusep::text from 1 for 2) = '22' then 'Pessoas EFPC'
  when substring(codigosusep::text from 1 for 2) = '21' then 'Sucursais no Exterior'
  when substring(codigosusep::text from 1 for 2) = '20' then 'Aceitações do Exterior'
  when substring(codigosusep::text from 1 for 2) = '19' then 'Saúde'
  when substring(codigosusep::text from 1 for 2) = '18' then 'Nucleares'
  when substring(codigosusep::text from 1 for 2) = '17' then 'Petróleo'
  when substring(codigosusep::text from 1 for 2) = '16' then 'Microsseguros'
  when substring(codigosusep::text from 1 for 2) = '15' then 'Aeronáuticos'
  when substring(codigosusep::text from 1 for 2) = '14' then 'Marítimos'
  when substring(codigosusep::text from 1 for 2) = '13' then 'Pessoas Individual'
  when substring(codigosusep::text from 1 for 2) = '12' then 'Outros'
  when substring(codigosusep::text from 1 for 2) = '11' then 'Rural'
  when substring(codigosusep::text from 1 for 2) = '10' then 'Habitacional'
  when substring(codigosusep::text from 1 for 1) = '9' then 'Pessoas Coletivo' 
  when substring(codigosusep::text from 1 for 1) = '8' then 'Crédito' 
  when substring(codigosusep::text from 1 for 1) = '7' then 'Riscos Financeiros' 
  when substring(codigosusep::text from 1 for 1) = '6' then 'Transportes' 
  when substring(codigosusep::text from 1 for 1) = '5' then 'Automóvel' 
  when substring(codigosusep::text from 1 for 1) = '4' then 'Cascos' 
  when substring(codigosusep::text from 1 for 1) = '3' then 'Responsabilidades' 
  when substring(codigosusep::text from 1 for 1) = '2' then 'Riscos Especiais' 
  when substring(codigosusep::text from 1 for 1) = '1' then 'Patrimonial' 
	else null end as nome_grupo
, empresa
, periodo
, to_date(periodo, 'YYYYMM') AS data_formatada
, estado
, case    when estado in ('ac', 'ap', 'am', 'pa', 'ro', 'rr', 'to') then 'norte'
        when estado in ('al', 'ba', 'ce', 'ma', 'pb', 'pe', 'pi', 'rn', 'se') then 'nordeste'
        when estado in ('df', 'go', 'ms', 'mt') then 'centro-oeste'
        when estado in ('es', 'mg', 'rj', 'sp') then 'sudeste'
        when estado in ('pr', 'rs', 'sc') then 'sul'
        else 'outra região'
   		end as regiao
, valor

from public.premios_susep2