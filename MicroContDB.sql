CREATE DATABASE IF NOT EXISTS SmartPlant;
USE SmartPlant;

CREATE TABLE sensors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL,
    unit VARCHAR(10) NOT NULL
);

CREATE TABLE sensor_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT NOT NULL,
    value FLOAT NOT NULL,
    reading_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
);

CREATE TABLE actuators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL
);

CREATE TABLE actuator_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    actuator_id INT NOT NULL,
    action VARCHAR(20) NOT NULL,
    action_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (actuator_id) REFERENCES actuators(id) ON DELETE CASCADE
);

CREATE TABLE alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT NOT NULL,
    message TEXT NOT NULL,
    alert_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
);

-- Sample data
INSERT INTO sensors (name, type, unit) VALUES
('Talaj szenzor', 'nedvesség', '%'),
('Hőmérő', 'hőmérséklet', '°C');

INSERT INTO sensor_readings (sensor_id, value) VALUES
(1, 28.5),
(2, 23.7);

INSERT INTO actuators (name, type) VALUES
('Vízpumpa 1', 'szivattyú');

INSERT INTO actuator_log (actuator_id, action) VALUES
(1, 'BE');

INSERT INTO alerts (sensor_id, message) VALUES
(1, 'Alacsony nedvesség – öntözés szükséges!');