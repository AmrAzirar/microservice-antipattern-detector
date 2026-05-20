package com.example;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class CommonDataController {

    @GetMapping("/products")
    public Object getProducts() { return null; }

    @PostMapping("/products")
    public Object createProduct() { return null; }

    @GetMapping("/products/{id}")
    public Object getProduct() { return null; }

    @PutMapping("/products/{id}")
    public Object updateProduct() { return null; }

    @DeleteMapping("/products/{id}")
    public Object deleteProduct() { return null; }

    @GetMapping("/categories")
    public Object getCategories() { return null; }

    @PostMapping("/categories")
    public Object createCategory() { return null; }

    @GetMapping("/orders")
    public Object getOrders() { return null; }

    @PostMapping("/orders")
    public Object createOrder() { return null; }

    @GetMapping("/orders/{id}")
    public Object getOrder() { return null; }

    @PutMapping("/orders/{id}")
    public Object updateOrder() { return null; }

    @DeleteMapping("/orders/{id}")
    public Object deleteOrder() { return null; }

    @GetMapping("/users")
    public Object getUsers() { return null; }

    @GetMapping("/reviews")
    public Object getReviews() { return null; }

    @PostMapping("/reviews")
    public Object createReview() { return null; }

    @GetMapping("/dashboard")
    public Object getDashboard() { return null; }
}