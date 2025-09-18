const { app } = require('electron');
const path = require('path');
const fs = require('fs');

class PerformanceMonitor {
    constructor(logger) {
        this.logger = logger;
        this.metrics = {
            startup: {
                startTime: Date.now(),
                endTime: null,
                duration: null
            },
            memory: {
                initial: 0,
                current: 0,
                peak: 0,
                history: []
            },
            cpu: {
                usage: 0,
                history: []
            },
            database: {
                queries: 0,
                queryTime: 0,
                averageQueryTime: 0
            },
            pdf: {
                generated: 0,
                totalTime: 0,
                averageTime: 0
            },
            errors: {
                count: 0,
                rate: 0
            }
        };
        
        this.monitoringInterval = null;
        this.isMonitoring = false;
        
        this.setupMonitoring();
    }
    
    setupMonitoring() {
        // Inizializza le metriche di memoria
        this.updateMemoryMetrics();
        
        // Avvia il monitoraggio periodico
        this.startMonitoring();
    }
    
    startMonitoring() {
        if (this.isMonitoring) {
            return;
        }
        
        this.isMonitoring = true;
        
        // Monitora ogni 30 secondi
        this.monitoringInterval = setInterval(() => {
            this.updateMemoryMetrics();
            this.updateCpuMetrics();
            this.cleanupOldData();
        }, 30000);
        
        this.logger.info('Monitoraggio performance avviato');
    }
    
    stopMonitoring() {
        if (this.monitoringInterval) {
            clearInterval(this.monitoringInterval);
            this.monitoringInterval = null;
        }
        
        this.isMonitoring = false;
        this.logger.info('Monitoraggio performance fermato');
    }
    
    updateMemoryMetrics() {
        try {
            const memUsage = process.memoryUsage();
            const currentMemory = memUsage.heapUsed;
            
            if (this.metrics.memory.initial === 0) {
                this.metrics.memory.initial = currentMemory;
            }
            
            this.metrics.memory.current = currentMemory;
            this.metrics.memory.peak = Math.max(this.metrics.memory.peak, currentMemory);
            
            // Aggiungi alla cronologia (mantieni solo gli ultimi 100 punti)
            this.metrics.memory.history.push({
                timestamp: Date.now(),
                value: currentMemory
            });
            
            if (this.metrics.memory.history.length > 100) {
                this.metrics.memory.history.shift();
            }
            
        } catch (error) {
            this.logger.error('Errore aggiornamento metriche memoria', { error: error.message });
        }
    }
    
    updateCpuMetrics() {
        try {
            const cpuUsage = process.cpuUsage();
            const usage = (cpuUsage.user + cpuUsage.system) / 1000000; // Converti in secondi
            
            this.metrics.cpu.usage = usage;
            
            // Aggiungi alla cronologia
            this.metrics.cpu.history.push({
                timestamp: Date.now(),
                value: usage
            });
            
            if (this.metrics.cpu.history.length > 100) {
                this.metrics.cpu.history.shift();
            }
            
        } catch (error) {
            this.logger.error('Errore aggiornamento metriche CPU', { error: error.message });
        }
    }
    
    cleanupOldData() {
        const now = Date.now();
        const maxAge = 24 * 60 * 60 * 1000; // 24 ore
        
        // Pulisci cronologia memoria
        this.metrics.memory.history = this.metrics.memory.history.filter(
            entry => now - entry.timestamp < maxAge
        );
        
        // Pulisci cronologia CPU
        this.metrics.cpu.history = this.metrics.cpu.history.filter(
            entry => now - entry.timestamp < maxAge
        );
    }
    
    // Metodi per registrare eventi specifici
    
    recordStartupComplete() {
        this.metrics.startup.endTime = Date.now();
        this.metrics.startup.duration = this.metrics.startup.endTime - this.metrics.startup.startTime;
        
        this.logger.info('Avvio applicazione completato', {
            duration: this.metrics.startup.duration
        });
    }
    
    recordDatabaseQuery(queryTime) {
        this.metrics.database.queries++;
        this.metrics.database.queryTime += queryTime;
        this.metrics.database.averageQueryTime = 
            this.metrics.database.queryTime / this.metrics.database.queries;
    }
    
    recordPdfGeneration(generationTime) {
        this.metrics.pdf.generated++;
        this.metrics.pdf.totalTime += generationTime;
        this.metrics.pdf.averageTime = 
            this.metrics.pdf.totalTime / this.metrics.pdf.generated;
    }
    
    recordError() {
        this.metrics.errors.count++;
        
        // Calcola il tasso di errori (errori per ora)
        const now = Date.now();
        const oneHourAgo = now - (60 * 60 * 1000);
        
        // Questo è un calcolo semplificato - in un'implementazione reale
        // dovresti tenere traccia del timestamp di ogni errore
        this.metrics.errors.rate = this.metrics.errors.count / 
            ((now - this.metrics.startup.startTime) / (60 * 60 * 1000));
    }
    
    // Metodi per ottenere le metriche
    
    getMetrics() {
        return {
            ...this.metrics,
            uptime: Date.now() - this.metrics.startup.startTime,
            isMonitoring: this.isMonitoring
        };
    }
    
    getMemoryUsage() {
        return {
            current: this.metrics.memory.current,
            initial: this.metrics.memory.initial,
            peak: this.metrics.memory.peak,
            growth: this.metrics.memory.current - this.metrics.memory.initial,
            growthPercentage: ((this.metrics.memory.current - this.metrics.memory.initial) / 
                this.metrics.memory.initial) * 100
        };
    }
    
    getCpuUsage() {
        return {
            current: this.metrics.cpu.usage,
            average: this.calculateAverage(this.metrics.cpu.history),
            peak: Math.max(...this.metrics.cpu.history.map(h => h.value), 0)
        };
    }
    
    getDatabaseStats() {
        return {
            totalQueries: this.metrics.database.queries,
            totalQueryTime: this.metrics.database.queryTime,
            averageQueryTime: this.metrics.database.averageQueryTime,
            queriesPerSecond: this.metrics.database.queries / 
                ((Date.now() - this.metrics.startup.startTime) / 1000)
        };
    }
    
    getPdfStats() {
        return {
            totalGenerated: this.metrics.pdf.generated,
            totalTime: this.metrics.pdf.totalTime,
            averageTime: this.metrics.pdf.averageTime
        };
    }
    
    getErrorStats() {
        return {
            totalErrors: this.metrics.errors.count,
            errorRate: this.metrics.errors.rate
        };
    }
    
    // Metodi di utilità
    
    calculateAverage(history) {
        if (history.length === 0) return 0;
        
        const sum = history.reduce((acc, entry) => acc + entry.value, 0);
        return sum / history.length;
    }
    
    // Metodo per esportare le metriche
    exportMetrics(filePath) {
        try {
            const exportData = {
                timestamp: new Date().toISOString(),
                metrics: this.getMetrics(),
                summary: {
                    memory: this.getMemoryUsage(),
                    cpu: this.getCpuUsage(),
                    database: this.getDatabaseStats(),
                    pdf: this.getPdfStats(),
                    errors: this.getErrorStats()
                }
            };
            
            fs.writeFileSync(filePath, JSON.stringify(exportData, null, 2));
            
            this.logger.info('Metriche performance esportate', { filePath });
            
            return { success: true };
        } catch (error) {
            this.logger.error('Errore esportazione metriche', { error: error.message });
            return { success: false, error: error.message };
        }
    }
    
    // Metodo per resettare le metriche
    resetMetrics() {
        this.metrics = {
            startup: {
                startTime: Date.now(),
                endTime: null,
                duration: null
            },
            memory: {
                initial: 0,
                current: 0,
                peak: 0,
                history: []
            },
            cpu: {
                usage: 0,
                history: []
            },
            database: {
                queries: 0,
                queryTime: 0,
                averageQueryTime: 0
            },
            pdf: {
                generated: 0,
                totalTime: 0,
                averageTime: 0
            },
            errors: {
                count: 0,
                rate: 0
            }
        };
        
        this.logger.info('Metriche performance resettate');
    }
    
    // Metodo per ottenere un report di performance
    getPerformanceReport() {
        const metrics = this.getMetrics();
        const memory = this.getMemoryUsage();
        const cpu = this.getCpuUsage();
        const database = this.getDatabaseStats();
        const pdf = this.getPdfStats();
        const errors = this.getErrorStats();
        
        return {
            timestamp: new Date().toISOString(),
            uptime: metrics.uptime,
            startup: {
                duration: metrics.startup.duration,
                status: metrics.startup.duration ? 'completed' : 'in-progress'
            },
            memory: {
                current: Math.round(memory.current / 1024 / 1024) + ' MB',
                peak: Math.round(memory.peak / 1024 / 1024) + ' MB',
                growth: Math.round(memory.growth / 1024 / 1024) + ' MB',
                growthPercentage: Math.round(memory.growthPercentage) + '%'
            },
            cpu: {
                current: Math.round(cpu.current * 100) / 100 + ' seconds',
                average: Math.round(cpu.average * 100) / 100 + ' seconds',
                peak: Math.round(cpu.peak * 100) / 100 + ' seconds'
            },
            database: {
                totalQueries: database.totalQueries,
                averageQueryTime: Math.round(database.averageQueryTime) + ' ms',
                queriesPerSecond: Math.round(database.queriesPerSecond * 100) / 100
            },
            pdf: {
                totalGenerated: pdf.totalGenerated,
                averageTime: Math.round(pdf.averageTime) + ' ms'
            },
            errors: {
                totalErrors: errors.totalErrors,
                errorRate: Math.round(errors.errorRate * 100) / 100 + ' errors/hour'
            }
        };
    }
}

module.exports = PerformanceMonitor;
