package com.example.fileprocessor;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.List;
import java.util.ArrayList;

/**
 * 一个线程安全的多线程文件读取器。
 * 使用线程池和读写锁来管理对文件内容的并发访问。
 */
public class ThreadSafeFileReader {

    private final String filePath;
    private final List<String> fileLines;
    private final ReentrantReadWriteLock lock;
    private final ExecutorService executorService;
    private volatile boolean isFileLoaded = false;

    /**
     * 构造函数，初始化文件路径、内部存储结构和线程池。
     * @param filePath 要读取的文件路径
     * @param numberOfThreads 线程池大小
     */
    public ThreadSafeFileReader(String filePath, int numberOfThreads) {
        this.filePath = filePath;
        this.fileLines = new ArrayList<>();
        this.lock = new ReentrantReadWriteLock();
        this.executorService = Executors.newFixedThreadPool(numberOfThreads);
    }

    /**
     * 启动一个后台线程来加载文件内容。
     * 此方法立即返回，不等待加载完成。
     */
    public void loadFileAsync() {
        executorService.submit(() -> {
            try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
                String line;
                // 获取写锁以填充列表
                lock.writeLock().lock();
                try {
                    fileLines.clear(); // 清空旧内容（如果有）
                    while ((line = reader.readLine()) != null) {
                        fileLines.add(line);
                    }
                    isFileLoaded = true;
                } finally {
                    lock.writeLock().unlock();
                }
                System.out.println("File '" + filePath + "' loaded successfully with " + fileLines.size() + " lines.");
            } catch (IOException e) {
                System.err.println("Error reading file: " + e.getMessage());
                // 获取写锁以确保在出错时状态一致
                lock.writeLock().lock();
                try {
                    fileLines.clear();
                    isFileLoaded = false;
                } finally {
                    lock.writeLock().unlock();
                }
            }
        });
    }

    /**
     * 获取文件的总行数。
     * @return 文件行数，如果文件未加载则返回-1。
     */
    public int getLineCount() {
        // 获取读锁以访问列表大小
        lock.readLock().lock();
        try {
            if (!isFileLoaded) {
                return -1;
            }
            return fileLines.size();
        } finally {
            lock.readLock().unlock();
        }
    }

    /**
     * 获取指定行的内容。
     * @param lineNumber 行号 (从0开始)
     * @return 指定行的内容，如果行号无效或文件未加载则返回null。
     */
    public String getLine(int lineNumber) {
        // 获取读锁以访问列表元素
        lock.readLock().lock();
        try {
            if (!isFileLoaded || lineNumber < 0 || lineNumber >= fileLines.size()) {
                return null;
            }
            return fileLines.get(lineNumber);
        } finally {
            lock.readLock().unlock();
        }
    }

    /**
     * 提交一个任务到线程池中执行。任务可以是任何需要并发处理的逻辑。
     * @param task 要执行的Runnable任务
     */
    public void submitTask(Runnable task) {
        executorService.submit(task);
    }

    /**
     * 关闭读取器，释放线程池资源。
     * @param timeout 等待现有任务终止的超时时间（秒）
     * @throws InterruptedException 如果等待被中断
     */
    public void shutdown(long timeout) throws InterruptedException {
        executorService.shutdown();
        if (!executorService.awaitTermination(timeout, TimeUnit.SECONDS)) {
            System.err.println("Pool did not terminate in " + timeout + " seconds, forcing shutdown.");
            executorService.shutdownNow();
        }
    }

    /**
     * 主方法，用于演示如何使用ThreadSafeFileReader。
     */
    public static void main(String[] args) {
        String filePath = "../sample_data.txt";
        int numberOfThreads = 4;
        ThreadSafeFileReader reader = new ThreadSafeFileReader(filePath, numberOfThreads);

        // 异步加载文件
        reader.loadFileAsync();

        // 提交一些并发任务来读取文件
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            reader.submitTask(() -> {
                // 简单的自旋等待，直到文件加载完成
                while (!reader.isFileLoaded) {
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                }

                int lineCount = reader.getLineCount();
                if (lineCount > 0) {
                    // 随机读取几行
                    for (int j = 0; j < 3; j++) {
                        int randomLine = (int) (Math.random() * lineCount);
                        String content = reader.getLine(randomLine);
                        System.out.println("Task " + taskId + " read line " + randomLine + ": " + content);
                    }
                } else {
                    System.out.println("Task " + taskId + " found file not loaded or empty.");
                }
            });
        }

        // 关闭读取器
        try {
            reader.shutdown(10);
            System.out.println("File reader shut down gracefully.");
        } catch (InterruptedException e) {
            System.err.println("Shutdown interrupted: " + e.getMessage());
            Thread.currentThread().interrupt();
        }
    }
}