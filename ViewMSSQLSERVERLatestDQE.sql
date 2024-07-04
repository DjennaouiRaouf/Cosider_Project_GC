create view  tmp as (
    select d.id as id ,c.code_contrat ,c.avenant,d.prixProduit_id,d.qte,p.code_produits from DQE d ,Contrats c,Prix_Produit pp,Produit p
    where c.id = d.contrat_id and pp.id = d.prixProduit_id and p.code_produits=pp.produit_id
)

SELECT code_contrat,code_produits, SUM(qte) AS qte_cumule
 FROM tmp

    GROUP BY  code_contrat, code_produits







select * from
(SELECT code_contrat,code_produits, SUM(qte) AS qte_cumule
 FROM tmp

    GROUP BY  code_contrat, code_produits) as a
join
(select * from tmp)as b on b.code_produits=a.code_produits and a.code_contrat=b.code_contrat

where avenant=2