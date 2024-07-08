create view DQE_View as(select d.*,pp.produit_id,c.code_contrat,c.avenant from DQE d,Prix_Produit pp,Contrats c
where d.prixProduit_id = pp.id and c.id=d.contrat_id
);

select dv1.produit_id,dv1.code_contrat,sum(dv1.qte) as Qte,
(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat) avenant ,
(select dv3.contrat_id  from DQE_View dv3 where dv1.code_contrat=dv3.code_contrat and dv1.produit_id=dv3.produit_id and dv3.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) contrat_id,
(select dv4.id from DQE_View dv4 where dv1.code_contrat=dv4.code_contrat and dv1.produit_id=dv4.produit_id and dv4.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) id,
(select dv5.prixProduit_id from DQE_View dv5 where dv1.code_contrat=dv5.code_contrat and dv1.produit_id=dv5.produit_id and dv5.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) prixProduit_id,
(select dv6.rabais from DQE_View dv6 where dv1.code_contrat=dv6.code_contrat and dv1.produit_id=dv6.produit_id and dv6.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) rabais,
(select dv7.prix_transport from DQE_View dv7 where dv1.code_contrat=dv7.code_contrat and dv1.produit_id=dv7.produit_id and dv7.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) prix_transport,
(select dv8.est_bloquer from DQE_View dv8 where dv1.code_contrat=dv8.code_contrat and dv1.produit_id=dv8.produit_id and dv8.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) est_bloquer,
(select dv9.user_id from DQE_View dv9 where dv1.code_contrat=dv9.code_contrat and dv1.produit_id=dv9.produit_id and dv9.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) user_id,
(select dv10.date_modification from DQE_View dv10 where dv1.code_contrat=dv10.code_contrat and dv1.produit_id=dv10.produit_id and dv10.avenant=(select max(dv2.avenant) avenant  from DQE_View dv2 where code_contrat=dv2.code_contrat and dv1.produit_id=dv2.produit_id group by  dv2.code_contrat)) date_modification



from DQE_View dv1 where dv1.est_bloquer = 0 group by dv1.produit_id,dv1.code_contrat


/*********************************************************************************************/


create view DQE_View as(select d.*,pp.produit_id,c.code_contrat,c.avenant from DQE d,Prix_Produit pp,Contrats c
where d.prixProduit_id = pp.id and c.id=d.contrat_id
);



CREATE VIEW DQE_View_Cumule AS
SELECT
    dv1.produit_id,
    dv1.code_contrat,
    SUM(dv1.qte) AS Qte,
    MAX(dv2.avenant) AS avenant,
    dv3.contrat_id,
    dv4.id,
    dv5.prixProduit_id,
    dv6.rabais,
    dv7.prix_transport,
    dv8.est_bloquer,
    dv9.user_id,
    dv10.date_modification
FROM
    DQE_View dv1
    -- Subquery dv2 to find max avenant per produit_id and code_contrat
    LEFT JOIN (
        SELECT
            produit_id,
            code_contrat,
            MAX(avenant) AS avenant
        FROM
            DQE_View
        GROUP BY
            produit_id, code_contrat
    ) dv2 ON dv1.produit_id = dv2.produit_id
           AND dv1.code_contrat = dv2.code_contrat
    -- Join dv3 to get contrat_id for max avenant
    LEFT JOIN DQE_View dv3 ON dv1.produit_id = dv3.produit_id
                           AND dv1.code_contrat = dv3.code_contrat
                           AND dv2.avenant = dv3.avenant
    -- Join dv4 to get id for max avenant
    LEFT JOIN DQE_View dv4 ON dv1.produit_id = dv4.produit_id
                           AND dv1.code_contrat = dv4.code_contrat
                           AND dv2.avenant = dv4.avenant
    -- Join dv5 to get prixProduit_id for max avenant
    LEFT JOIN DQE_View dv5 ON dv1.produit_id = dv5.produit_id
                           AND dv1.code_contrat = dv5.code_contrat
                           AND dv2.avenant = dv5.avenant
    -- Join dv6 to get rabais for max avenant
    LEFT JOIN DQE_View dv6 ON dv1.produit_id = dv6.produit_id
                           AND dv1.code_contrat = dv6.code_contrat
                           AND dv2.avenant = dv6.avenant
    -- Join dv7 to get prix_transport for max avenant
    LEFT JOIN DQE_View dv7 ON dv1.produit_id = dv7.produit_id
                           AND dv1.code_contrat = dv7.code_contrat
                           AND dv2.avenant = dv7.avenant

    LEFT JOIN DQE_View dv8 ON dv1.produit_id = dv8.produit_id
                           AND dv1.code_contrat = dv8.code_contrat
                           AND dv2.avenant = dv8.avenant

    LEFT JOIN DQE_View dv9 ON dv1.produit_id = dv9.produit_id
                           AND dv1.code_contrat = dv9.code_contrat
                           AND dv2.avenant = dv9.avenant
    LEFT JOIN DQE_View dv10 ON dv1.produit_id = dv10.produit_id
                           AND dv1.code_contrat = dv10.code_contrat
                           AND dv2.avenant = dv10.avenant


GROUP BY
    dv1.produit_id, dv1.code_contrat, dv3.contrat_id, dv4.id, dv5.prixProduit_id, dv6.rabais, dv7.prix_transport
    ,dv8.est_bloquer,dv9.user_id,dv10.date_modification;






create view Contrats_View as(
SELECT co.* FROM Contrats co

JOIN (
    SELECT code_contrat, MAX(avenant) AS avenant
    FROM Contrats
    GROUP BY code_contrat
) latest ON co.code_contrat = latest.code_contrat
          AND co.avenant = latest.avenant

);

