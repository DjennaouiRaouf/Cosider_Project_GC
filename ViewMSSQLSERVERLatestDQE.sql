
/*******************************************************************************************************************************/
create view DQE_View as(select d.*,pp.produit_id,c.code_contrat,c.avenant from DQE d,Prix_Produit pp,Contrats c
where d.prixProduit_id = pp.id and c.id=d.contrat_id and  d.est_bloquer=0 and c.est_bloquer=0 and pp.est_bloquer=0
);


/*******************************************************************************************************************************/

CREATE VIEW DQE_View_Cumule AS(
SELECT
    dv4.id,
    dv1.produit_id,
    dv1.code_contrat,
    SUM(dv1.qte) AS Qte,
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
            MIN(avenant) AS avenant
        FROM
            DQE_View
        GROUP BY
            produit_id, code_contrat
    ) dv2 ON dv1.produit_id = dv2.produit_id
           AND dv1.code_contrat = dv2.code_contrat
    LEFT JOIN (
        SELECT
            produit_id,
            code_contrat,
            MAX(avenant) AS avenant
        FROM
            DQE_View
        GROUP BY
            produit_id, code_contrat
    ) dv0 ON dv1.produit_id = dv0.produit_id
           AND dv0.code_contrat = dv0.code_contrat

    -- Join dv4 to get id for min avenant
    LEFT JOIN DQE_View dv4 ON dv1.produit_id = dv4.produit_id
                           AND dv1.code_contrat = dv4.code_contrat
                           AND dv2.avenant = dv4.avenant
    -- Join dv5 to get prixProduit_id for max avenant
    LEFT JOIN DQE_View dv5 ON dv1.produit_id = dv5.produit_id
                           AND dv1.code_contrat = dv5.code_contrat
                           AND dv0.avenant = dv5.avenant
    -- Join dv6 to get rabais for max avenant
    LEFT JOIN DQE_View dv6 ON dv1.produit_id = dv6.produit_id
                           AND dv1.code_contrat = dv6.code_contrat
                           AND dv0.avenant = dv6.avenant
    -- Join dv7 to get prix_transport for max avenant
    LEFT JOIN DQE_View dv7 ON dv1.produit_id = dv7.produit_id
                           AND dv1.code_contrat = dv7.code_contrat
                           AND dv0.avenant = dv7.avenant

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
    dv1.produit_id, dv1.code_contrat,dv4.id, dv5.prixProduit_id, dv6.rabais, dv7.prix_transport
    ,dv8.est_bloquer,dv9.user_id,dv10.date_modification



);


/*******************************************************************************************************************************/

SELECT
    dv4.id,
    dv1.produit_id,
    dv1.code_contrat,
    SUM(dv1.qte) AS Qte,
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
            MIN(avenant) AS avenant
        FROM
            DQE_View
        GROUP BY
            produit_id, code_contrat
    ) dv2 ON dv1.produit_id = dv2.produit_id
           AND dv1.code_contrat = dv2.code_contrat
    LEFT JOIN (
        SELECT
            produit_id,
            code_contrat,
            MAX(avenant) AS avenant
        FROM
            DQE_View
        GROUP BY
            produit_id, code_contrat
    ) dv0 ON dv1.produit_id = dv0.produit_id
           AND dv0.code_contrat = dv0.code_contrat

    -- Join dv4 to get id for min avenant
    LEFT JOIN DQE_View dv4 ON dv1.produit_id = dv4.produit_id
                           AND dv1.code_contrat = dv4.code_contrat
                           AND dv2.avenant = dv4.avenant
    -- Join dv5 to get prixProduit_id for max avenant
    LEFT JOIN DQE_View dv5 ON dv1.produit_id = dv5.produit_id
                           AND dv1.code_contrat = dv5.code_contrat
                           AND dv0.avenant = dv5.avenant
    -- Join dv6 to get rabais for max avenant
    LEFT JOIN DQE_View dv6 ON dv1.produit_id = dv6.produit_id
                           AND dv1.code_contrat = dv6.code_contrat
                           AND dv0.avenant = dv6.avenant
    -- Join dv7 to get prix_transport for max avenant
    LEFT JOIN DQE_View dv7 ON dv1.produit_id = dv7.produit_id
                           AND dv1.code_contrat = dv7.code_contrat
                           AND dv0.avenant = dv7.avenant

    LEFT JOIN DQE_View dv8 ON dv1.produit_id = dv8.produit_id
                           AND dv1.code_contrat = dv8.code_contrat
                           AND dv2.avenant = dv8.avenant

    LEFT JOIN DQE_View dv9 ON dv1.produit_id = dv9.produit_id
                           AND dv1.code_contrat = dv9.code_contrat
                           AND dv2.avenant = dv9.avenant
    LEFT JOIN DQE_View dv10 ON dv1.produit_id = dv10.produit_id
                           AND dv1.code_contrat = dv10.code_contrat
                           AND dv2.avenant = dv10.avenant

where
    dv1.avenant in(0,1)

GROUP BY
    dv1.produit_id, dv1.code_contrat,dv4.id, dv5.prixProduit_id, dv6.rabais, dv7.prix_transport
    ,dv8.est_bloquer,dv9.user_id,dv10.date_modification





/*restaure log Avenant*/






/*******************************************************************************************************************************/




create view Contrats_View as(
SELECT co.* FROM Contrats co

JOIN (
    SELECT code_contrat, MAX(avenant) AS avenant
    FROM Contrats
    GROUP BY code_contrat
) latest ON co.code_contrat = latest.code_contrat
          AND co.avenant = latest.avenant

);

/*******************************************************************************************************************************/

create view DQE_View_Cumule as (
SELECT
    dv4.id,
    dv1.produit_id,
    dv1.code_contrat,
    dv3.avenant,
    SUM(dv1.qte) AS Qte,
    CONCAT(dv1.code_contrat, '(', dv3.avenant,')') as contrat_id,
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
            MIN(avenant) AS avenant
        FROM
            DQE_View
        GROUP BY
            produit_id, code_contrat
    ) dv2 ON dv1.produit_id = dv2.produit_id
           AND dv1.code_contrat = dv2.code_contrat
    LEFT JOIN (
        SELECT
            produit_id,
            code_contrat,
            MAX(avenant) AS avenant
        FROM
            DQE_View
        GROUP BY
            produit_id, code_contrat
    ) dv0 ON dv1.produit_id = dv0.produit_id
           AND dv0.code_contrat = dv0.code_contrat

    -- Join dv4 to get id for min avenant
    LEFT JOIN DQE_View dv4 ON dv1.produit_id = dv4.produit_id
                           AND dv1.code_contrat = dv4.code_contrat
                           AND dv2.avenant = dv4.avenant
    -- Join dv5 to get prixProduit_id for max avenant
    LEFT JOIN DQE_View dv5 ON dv1.produit_id = dv5.produit_id
                           AND dv1.code_contrat = dv5.code_contrat
                           AND dv0.avenant = dv5.avenant
    -- Join dv6 to get rabais for max avenant
    LEFT JOIN DQE_View dv6 ON dv1.produit_id = dv6.produit_id
                           AND dv1.code_contrat = dv6.code_contrat
                           AND dv0.avenant = dv6.avenant
    -- Join dv7 to get prix_transport for max avenant
    LEFT JOIN DQE_View dv7 ON dv1.produit_id = dv7.produit_id
                           AND dv1.code_contrat = dv7.code_contrat
                           AND dv0.avenant = dv7.avenant

    LEFT JOIN DQE_View dv8 ON dv1.produit_id = dv8.produit_id
                           AND dv1.code_contrat = dv8.code_contrat
                           AND dv2.avenant = dv8.avenant

    LEFT JOIN DQE_View dv9 ON dv1.produit_id = dv9.produit_id
                           AND dv1.code_contrat = dv9.code_contrat
                           AND dv2.avenant = dv9.avenant
    LEFT JOIN DQE_View dv10 ON dv1.produit_id = dv10.produit_id
                           AND dv1.code_contrat = dv10.code_contrat
                           AND dv2.avenant = dv10.avenant

        LEFT JOIN (
        SELECT
            code_contrat,
            MAX(avenant) AS avenant
        FROM
            DQE_View
        GROUP BY
            code_contrat
    ) dv3 ON dv1.code_contrat = dv3.code_contrat


GROUP BY
    dv1.produit_id, dv1.code_contrat,dv3.avenant,dv4.id, dv5.prixProduit_id, dv6.rabais, dv7.prix_transport
    ,dv8.est_bloquer,dv9.user_id,dv10.date_modification


);

/*******************************************************************************************************************************/




/*******************************************************************************************************************************/



create view Contrats_View as(
SELECT co.* FROM Contrats co

JOIN (
    SELECT code_contrat, MAX(avenant) AS avenant
    FROM Contrats
    GROUP BY code_contrat
) latest ON co.code_contrat = latest.code_contrat
          AND co.avenant = latest.avenant

);


/*******************************************************************************************************************************/