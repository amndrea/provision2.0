/* sostituire il numero 8 con l'ID della prefattura */
SELECT
	m.magazzino_lettera,
    l.conto_contabile,
    l.voce_spesa,
    l.centro_costo,
    SUM(pr.quantita * l.costo) AS totale_costo
FROM 
    mainapp_prefatturarighe pr
JOIN 
    mainapp_listino l ON pr.riga_listino_id = l.id
JOIN 
	mainapp_magazzino m ON l.magazzino_id = m.id
WHERE 
    pr.prefattura_id = 8
GROUP BY 
	m.magazzino_lettera, 
    l.conto_contabile,
    l.voce_spesa,
    l.centro_costo
ORDER BY 
    l.conto_contabile,
    l.voce_spesa,
    l.centro_costo;