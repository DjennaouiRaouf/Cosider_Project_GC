create view  tmp as (
    select d.id as id ,c.code_contrat ,c.avenant,d.prixProduit_id,d.qte,p.code_produits from DQE d ,Contrats c,Prix_Produit pp,Produit p
    where c.id = d.contrat_id and pp.id = d.prixProduit_id and p.code_produits=pp.produit_id
)

SELECT code_contrat,code_produits, SUM(qte) AS qte_cumule
 FROM tmp

    GROUP BY  code_contrat, code_produits







SELECT max(id),code_contrat,max(avenant)as avenant,code_produits,SUM(qte) AS qte_cumule,max(prixProduit_id)
FROM tmp
GROUP BY  code_contrat,code_produits;

