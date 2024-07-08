create view DQE_View as(select d.*,pp.produit_id,c.code_contrat,c.avenant from DQE d,Prix_Produit pp,Contrats c
where d.prixProduit_id = pp.id and c.id=d.contrat_id
);


create view DQE_View_Cumule as
(
select dv1.produit_id,dv1.code_contrat,sum(dv1.qte) as Qte,
(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat) avenant ,
(select dv3.contrat_id  from DQE_View dv3 where dv1.code_contrat=dv3.code_contrat and dv1.produit_id=dv3.produit_id and dv3.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) contrat_id,
(select dv4.id from DQE_View dv4 where dv1.code_contrat=dv4.code_contrat and dv1.produit_id=dv4.produit_id and dv4.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) id,
(select dv5.prixProduit_id from DQE_View dv5 where dv1.code_contrat=dv5.code_contrat and dv1.produit_id=dv5.produit_id and dv5.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) prixProduit_id,
(select dv6.rabais from DQE_View dv6 where dv1.code_contrat=dv6.code_contrat and dv1.produit_id=dv6.produit_id and dv6.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) rabais,
(select dv7.prix_transport from DQE_View dv7 where dv1.code_contrat=dv7.code_contrat and dv1.produit_id=dv7.produit_id and dv7.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) prix_transport

from DQE_View dv1 group by dv1.produit_id,dv1.code_contrat
);








