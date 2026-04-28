-- Création de la base de données
CREATE DATABASE IF NOT EXISTS fidelite_client;
USE fidelite_client;

-- Table clients
CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    ville VARCHAR(100),
    date_inscription DATE NOT NULL
);

-- Table programmes
CREATE TABLE programmes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    points_minimum INT NOT NULL,
    avantage VARCHAR(200)
);

-- Table many-to-many : client_programme
CREATE TABLE client_programme (
    client_id INT NOT NULL,
    programme_id INT NOT NULL,
    date_adhesion DATE NOT NULL,
    PRIMARY KEY (client_id, programme_id),
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (programme_id) REFERENCES programmes(id)
);

-- Table transactions
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    montant DECIMAL(10,2) NOT NULL,
    points_gagnes INT NOT NULL,
    date_transaction DATE NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Table recompenses
CREATE TABLE recompenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    description VARCHAR(200) NOT NULL,
    points_utilises INT NOT NULL,
    date_echange DATE NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);
-- Insertion des programmes
INSERT INTO programmes (nom, points_minimum, avantage) VALUES
('Bronze', 0, 'Accès aux offres de base'),
('Silver', 500, 'Livraison gratuite + 5% de réduction'),
('Gold', 1500, 'Livraison express + 10% de réduction + accès VIP');

-- Insertion des clients
INSERT INTO clients (nom, email, ville, date_inscription) VALUES
('Alice Martin', 'alice@email.com', 'Paris', '2023-01-15'),
('Bob Dupont', 'bob@email.com', 'Lyon', '2023-02-20'),
('Clara Petit', 'clara@email.com', 'Marseille', '2023-03-10'),
('David Moreau', 'david@email.com', 'Paris', '2023-04-05'),
('Emma Leroy', 'emma@email.com', 'Bordeaux', '2023-05-12'),
('François Blanc', 'francois@email.com', 'Lyon', '2023-06-18'),
('Grace Dubois', 'grace@email.com', 'Paris', '2023-07-22'),
('Hugo Bernard', 'hugo@email.com', 'Nantes', '2023-08-30'),
('Inès Thomas', 'ines@email.com', 'Toulouse', '2023-09-14'),
('Jules Robert', 'jules@email.com', 'Paris', '2023-10-01');

-- Insertion des transactions
INSERT INTO transactions (client_id, montant, points_gagnes, date_transaction) VALUES
(1, 120.50, 120, '2024-01-10'),
(1, 340.00, 340, '2024-02-15'),
(1, 89.99, 89, '2024-03-20'),
(2, 250.00, 250, '2024-01-25'),
(2, 175.50, 175, '2024-03-05'),
(3, 890.00, 890, '2024-02-10'),
(3, 450.00, 450, '2024-04-01'),
(4, 60.00, 60, '2024-01-30'),
(5, 1200.00, 1200, '2024-02-20'),
(5, 800.00, 800, '2024-03-15'),
-- ============================================
-- REQUÊTES SELECT
-- ============================================

-- 1. Clients de Paris ordonnés par date d'inscription
SELECT nom, email, date_inscription 
FROM clients 
WHERE ville = 'Paris' 
ORDER BY date_inscription DESC;

-- 2. Total des points gagnés par client
SELECT client_id, SUM(points_gagnes) AS total_points
FROM transactions
GROUP BY client_id
ORDER BY total_points DESC;

-- 3. Clients ayant plus de 500 points
SELECT client_id, SUM(points_gagnes) AS total_points
FROM transactions
GROUP BY client_id
HAVING SUM(points_gagnes) > 500;

-- 4. Top 5 des clients par montant dépensé
SELECT client_id, SUM(montant) AS total_depense
FROM transactions
GROUP BY client_id
ORDER BY total_depense DESC
LIMIT 5;

-- 5. Jointure 3 tables : clients + transactions + recompenses
SELECT c.nom, SUM(t.points_gagnes) AS points_gagnes, 
       COUNT(r.id) AS nb_recompenses
FROM clients c
JOIN transactions t ON c.id = t.client_id
LEFT JOIN recompenses r ON c.id = r.client_id
GROUP BY c.id, c.nom;

-- Sous-requête : clients avec plus de points que la moyenne
SELECT nom, email FROM clients
WHERE id IN (
    SELECT client_id FROM transactions
    GROUP BY client_id
    HAVING SUM(points_gagnes) > (SELECT AVG(points_gagnes) FROM transactions)
);

-- Vue : scoring fidélité
CREATE VIEW vue_scoring AS
SELECT c.nom, c.email, c.ville,
       SUM(t.points_gagnes) AS total_points,
       COUNT(t.id) AS nb_achats,
       SUM(t.montant) AS total_depense
FROM clients c
JOIN transactions t ON c.id = t.client_id
GROUP BY c.id, c.nom, c.email, c.ville;

