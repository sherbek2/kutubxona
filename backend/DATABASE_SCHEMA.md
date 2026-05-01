# Kutubxona Platformasi - Database Schema Design

## Database System

- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Connection Pool**: asyncpg

---

## Entity Relationship Diagram (ERD)

```
Users (1) -----> (M) Books
Users (1) -----> (M) Stores
Users (1) -----> (M) Reviews
Users (1) -----> (M) Messages
Users (1) -----> (M) Notifications
Users (1) -----> (M) Favorites

Stores (1) -----> (M) StoreBooks
Stores (1) -----> (M) Reviews

Books (1) -----> (M) Reviews
Books (1) -----> (M) BookImages
Books (1) -----> (M) Favorites

Categories (1) -----> (M) Books
Categories (1) -----> (M) StoreBooks

Conversations (M) -----> (M) Messages
Users (M) -----> (M) Conversations (ConversationParticipants)
```

---

## Tables

### 1. users

Foydalanuvchilar jadvali

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(500),
    bio TEXT,
    location VARCHAR(200),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    email_verified BOOLEAN DEFAULT FALSE,
    phone_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_blocked BOOLEAN DEFAULT FALSE,
    role VARCHAR(20) DEFAULT 'user', -- user, admin, moderator
    rating DECIMAL(3, 2) DEFAULT 0.00,
    total_reviews INTEGER DEFAULT 0,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_location ON users(latitude, longitude);
CREATE INDEX idx_users_rating ON users(rating);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### 2. categories

Kategoriyalar jadvali

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    parent_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_parent_id ON categories(parent_id);
CREATE INDEX idx_categories_sort_order ON categories(sort_order);
```

### 3. books

Kitoblar e'lonlari jadvali

```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    language VARCHAR(50) NOT NULL,
    year INTEGER,
    pages INTEGER,
    isbn VARCHAR(20),
    condition VARCHAR(20) DEFAULT 'new', -- new, like_new, good, fair
    type VARCHAR(20) NOT NULL, -- sell, free, rent
    price INTEGER,
    rent_price INTEGER,
    rent_duration VARCHAR(20), -- daily, weekly, monthly
    location VARCHAR(200),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    seller_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'active', -- active, sold, rented, deleted
    is_featured BOOLEAN DEFAULT FALSE,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    contact_count INTEGER DEFAULT 0,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_books_seller_id ON books(seller_id);
CREATE INDEX idx_books_category_id ON books(category_id);
CREATE INDEX idx_books_type ON books(type);
CREATE INDEX idx_books_status ON books(status);
CREATE INDEX idx_books_price ON books(price);
CREATE INDEX idx_books_location ON books(latitude, longitude);
CREATE INDEX idx_books_created_at ON books(created_at);
CREATE INDEX idx_books_title ON books USING gin(to_tsvector('english', title));
CREATE INDEX idx_books_author ON books USING gin(to_tsvector('english', author));
```

### 4. book_images

Kitob rasmlari jadvali

```sql
CREATE TABLE book_images (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    alt_text VARCHAR(200),
    sort_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_book_images_book_id ON book_images(book_id);
CREATE INDEX idx_book_images_sort_order ON book_images(sort_order);
```

### 5. stores

Kutubxonalar va kitob do'konlari jadvali

```sql
CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL, -- bookstore, library, reading_cafe, etc.
    description TEXT NOT NULL,
    address VARCHAR(300) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    website VARCHAR(200),
    facebook VARCHAR(100),
    instagram VARCHAR(100),
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'active', -- active, inactive, suspended
    is_verified BOOLEAN DEFAULT FALSE,
    rating DECIMAL(3, 2) DEFAULT 0.00,
    total_reviews INTEGER DEFAULT 0,
    followers_count INTEGER DEFAULT 0,
    books_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_stores_owner_id ON stores(owner_id);
CREATE INDEX idx_stores_category ON stores(category);
CREATE INDEX idx_stores_status ON stores(status);
CREATE INDEX idx_stores_location ON stores(latitude, longitude);
CREATE INDEX idx_stores_rating ON stores(rating);
CREATE INDEX idx_stores_created_at ON stores(created_at);
CREATE INDEX idx_stores_name ON stores USING gin(to_tsvector('english', name));
```

### 6. store_opening_hours

Kutubxona ish vaqtlari jadvali

```sql
CREATE TABLE store_opening_hours (
    id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    day_of_week VARCHAR(10) NOT NULL, -- monday, tuesday, etc.
    open_time TIME,
    close_time TIME,
    is_closed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE UNIQUE INDEX idx_store_opening_hours_store_day ON store_opening_hours(store_id, day_of_week);
```

### 7. store_features

Kutubxona xususiyatlari jadvali

```sql
CREATE TABLE store_features (
    id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    feature_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE UNIQUE INDEX idx_store_features_store_feature ON store_features(store_id, feature_name);
```

### 8. store_books

Kutubxonadagi kitoblar jadvali

```sql
CREATE TABLE store_books (
    id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    price INTEGER NOT NULL,
    stock INTEGER DEFAULT 1,
    isbn VARCHAR(20),
    image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_store_books_store_id ON store_books(store_id);
CREATE INDEX idx_store_books_category_id ON store_books(category_id);
CREATE INDEX idx_store_books_price ON store_books(price);
CREATE INDEX idx_store_books_title ON store_books USING gin(to_tsvector('english', title));
```

### 9. store_images

Kutubxona rasmlari jadvali

```sql
CREATE TABLE store_images (
    id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    alt_text VARCHAR(200),
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_store_images_store_id ON store_images(store_id);
CREATE INDEX idx_store_images_sort_order ON store_images(sort_order);
```

### 10. reviews

Sharhlar va reytinglar jadvali

```sql
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    reviewer_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    target_type VARCHAR(20) NOT NULL, -- book, store
    target_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    is_verified BOOLEAN DEFAULT FALSE, -- admin tomonidan tasdiqlangan
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(reviewer_id, target_type, target_id)
);

-- Indexes
CREATE INDEX idx_reviews_reviewer_id ON reviews(reviewer_id);
CREATE INDEX idx_reviews_target ON reviews(target_type, target_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_reviews_created_at ON reviews(created_at);
```

### 11. conversations

Suhbatlar jadvali

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 12. conversation_participants

Suhbat ishtirokchilari jadvali

```sql
CREATE TABLE conversation_participants (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_read_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(conversation_id, user_id)
);

-- Indexes
CREATE INDEX idx_conversation_participants_conversation_id ON conversation_participants(conversation_id);
CREATE INDEX idx_conversation_participants_user_id ON conversation_participants(user_id);
```

### 13. messages

Xabarlar jadvali

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    type VARCHAR(20) DEFAULT 'text', -- text, image, file
    file_url VARCHAR(500),
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_is_read ON messages(is_read);
```

### 14. notifications

Bildirishnomalar jadvali

```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL, -- new_message, book_liked, review_added, etc.
    data JSONB, -- qo'shimcha ma'lumotlar
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);
```

### 15. favorites

Sevimlilar jadvali

```sql
CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    item_type VARCHAR(20) NOT NULL, -- book, store
    item_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, item_type, item_id)
);

-- Indexes
CREATE INDEX idx_favorites_user_id ON favorites(user_id);
CREATE INDEX idx_favorites_item ON favorites(item_type, item_id);
```

### 16. user_sessions

Foydalanuvchi sessiyalari jadvali

```sql
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_session_token ON user_sessions(session_token);
CREATE INDEX idx_user_sessions_refresh_token ON user_sessions(refresh_token);
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at);
```

### 17. reports

Shikoyatlar jadvali

```sql
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    reporter_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    target_type VARCHAR(20) NOT NULL, -- book, store, user
    target_id INTEGER NOT NULL,
    reason VARCHAR(50) NOT NULL, -- spam, inappropriate, fake, other
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending', -- pending, reviewed, resolved, dismissed
    admin_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_reports_reporter_id ON reports(reporter_id);
CREATE INDEX idx_reports_target ON reports(target_type, target_id);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_reports_created_at ON reports(created_at);
```

### 18. audit_logs

Audit log jadvali (admin actions)

```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    admin_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    target_type VARCHAR(50),
    target_id INTEGER,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_audit_logs_admin_id ON audit_logs(admin_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_target ON audit_logs(target_type, target_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

---

## Triggers and Functions

### Update Timestamps

```sql
-- updated_at ni avtomatik yangilash uchun trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggerlar
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_books_updated_at BEFORE UPDATE ON books
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stores_updated_at BEFORE UPDATE ON stores
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_store_books_updated_at BEFORE UPDATE ON store_books
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reviews_updated_at BEFORE UPDATE ON reviews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reports_updated_at BEFORE UPDATE ON reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### Update Book Stats

```sql
-- Kitob statistikasini yangilash
CREATE OR REPLACE FUNCTION update_book_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE books SET like_count = like_count + 1 WHERE id = NEW.book_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE books SET like_count = like_count - 1 WHERE id = OLD.book_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- Trigger (favorites jadvali uchun)
CREATE TRIGGER update_book_like_count AFTER INSERT OR DELETE ON favorites
    FOR EACH ROW EXECUTE FUNCTION update_book_stats();
```

### Update Store Stats

```sql
-- Kutubxona statistikasini yangilash
CREATE OR REPLACE FUNCTION update_store_stats()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE stores SET 
        books_count = (SELECT COUNT(*) FROM store_books WHERE store_id = COALESCE(NEW.store_id, OLD.store_id) AND is_active = TRUE),
        total_reviews = (SELECT COUNT(*) FROM reviews WHERE target_type = 'store' AND target_id = COALESCE(NEW.store_id, OLD.store_id)),
        rating = COALESCE((SELECT AVG(rating) FROM reviews WHERE target_type = 'store' AND target_id = COALESCE(NEW.store_id, OLD.store_id)), 0)
    WHERE id = COALESCE(NEW.store_id, OLD.store_id);
    
    RETURN COALESCE(NEW, OLD);
END;
$$ language 'plpgsql';

-- Triggerlar
CREATE TRIGGER update_store_stats_trigger AFTER INSERT OR UPDATE OR DELETE ON store_books
    FOR EACH ROW EXECUTE FUNCTION update_store_stats();

CREATE TRIGGER update_store_stats_reviews_trigger AFTER INSERT OR UPDATE OR DELETE ON reviews
    FOR EACH ROW EXECUTE FUNCTION update_store_stats();
```

---

## Views

### User Stats View

```sql
CREATE VIEW user_stats AS
SELECT 
    u.id,
    u.first_name,
    u.last_name,
    u.email,
    u.rating,
    u.total_reviews,
    COUNT(DISTINCT b.id) as total_books,
    COUNT(DISTINCT CASE WHEN b.status = 'active' THEN b.id END) as active_books,
    COUNT(DISTINCT s.id) as total_stores,
    COUNT(DISTINCT f.id) as total_favorites,
    u.created_at
FROM users u
LEFT JOIN books b ON u.id = b.seller_id
LEFT JOIN stores s ON u.id = s.owner_id
LEFT JOIN favorites f ON u.id = f.user_id
GROUP BY u.id, u.first_name, u.last_name, u.email, u.rating, u.total_reviews, u.created_at;
```

### Book Details View

```sql
CREATE VIEW book_details AS
SELECT 
    b.*,
    c.name as category_name,
    u.first_name || ' ' || u.last_name as seller_name,
    u.avatar_url as seller_avatar,
    u.rating as seller_rating,
    COALESCE(AVG(r.rating), 0) as avg_rating,
    COUNT(r.id) as review_count,
    COUNT(DISTINCT f.id) as favorite_count,
    STRING_AGG(bi.image_url, ',' ORDER BY bi.sort_order) as images
FROM books b
LEFT JOIN categories c ON b.category_id = c.id
LEFT JOIN users u ON b.seller_id = u.id
LEFT JOIN reviews r ON r.target_type = 'book' AND r.target_id = b.id
LEFT JOIN favorites f ON f.item_type = 'book' AND f.item_id = b.id
LEFT JOIN book_images bi ON b.id = bi.book_id
GROUP BY b.id, c.name, u.first_name, u.last_name, u.avatar_url, u.rating;
```

---

## Data Seeding

### Categories

```sql
INSERT INTO categories (name, slug, description) VALUES
('Badiiy adabiyot', 'badiiy-adabiyot', 'Romanlar, hikoyalar, she''riyat'),
('Ilmiy adabiyot', 'ilmiy-adabiyot', 'Ilmiy asarlar, monografiyalar'),
('Darsliklar', 'darsliklar', 'Maktab va universitet darsliklari'),
('Bolalar adabiyoti', 'bolalar-adabiyoti', 'Bolalar uchun kitoblar'),
('Xorijiy adabiyot', 'xorijiy-adabiyot', 'Chet tillardagi kitoblar'),
('Tarix', 'tarix', 'Tarixiy asarlar'),
('Falsafa', 'falsafa', 'Falsafiy asarlar'),
('Psixologiya', 'psixologiya', 'Psixologiya kitoblari'),
('Biznes', 'biznes', 'Biznes va iqtisodiyot'),
('Diniy adabiyot', 'diniy-adabiyot', 'Diniy kitoblar'),
('Boshqa', 'boshqa', 'Boshqa toifalar');
```

---

## Performance Optimizations

### Partitioning

- **books** jadvalini yil bo'yicha partition qilish
- **messages** jadvalini oy bo'yicha partition qilish
- **notifications** jadvalini oy bo'yicha partition qilish

### Indexing Strategy

- Composite indexes for frequently queried columns
- Partial indexes for filtered queries
- GIN indexes for full-text search
- BRIN indexes for time-series data

### Caching Strategy

- Redis da user sessiyalari
- Popular books va stores cache
- Category tree cache
- User permissions cache

---

## Backup Strategy

- Daily full backups
- Hourly transaction log backups
- Point-in-time recovery support
- Backups encrypted and stored in multiple locations

---

## Security Considerations

- Row Level Security (RLS) for multi-tenant data
- Database connection encryption
- Regular security updates
- Audit logging for sensitive operations
- Data anonymization for development

---

## Migration Strategy

- Alembic for schema migrations
- Version-controlled migration files
- Rollback support
- Zero-downtime deployment support
