# نموذج البيانات وتخطيط الجداول

## 1. المبادئ العامة
- كل سجل مرتبط بمشروع عبر `project_id` (باستثناء الكيانات العالمية مثل المستخدمين، الموردين).
- الأعمدة المشتركة: `id` UUID، `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`, `deleted_by`.
- تفعيل **Row Level Security** مع سياسات خاصة بكل دور (Admin، Projects Director، Project Manager، Supervisor، Viewer، Trial).
- الاحتفاظ بسجلات التدقيق في جدول منفصل `audit_logs` مع JSON قبل/بعد.

## 2. الجداول الأساسية
### 2.1 المستخدمون والأدوار
- `users` (Supabase Auth): البريد الإلكتروني، الحالة.
- `user_profiles`: الاسم، اللغة، الهاتف، الدور الأساسي، إعدادات الإشعارات، quiet_hours.
- `user_roles_projects`: ربط المستخدمين بالمشاريع مع الدور (لـ Project Manager/Supervisor/Viewer).
- `role_permissions`: تعريف القدرات حسب الدور، يسمح بالتخصيص من لوحة الإدارة.

### 2.2 المشاريع والميزانيات
- `projects`: `code` فريد، `name`, `client`, `currency`, `budget_amount`, `start_date`, `end_date`, `status`.
- `project_cost_codes`: التصنيفات البسيطة، مرتبطة بالمشروع.
- `project_settings`: إعدادات متقدمة مثل تحذيرات الميزانية، تفعيل المساعد، نسب التحذير.

### 2.3 جدول الكميات (BOQ)
- `boq_items`: `project_id`, `cost_code_id`, `index`, `description`, `unit`, `contract_qty`, `unit_price`, `executed_qty`, `notes`.
- قيود: `executed_qty <= contract_qty` إلا إذا `override_reason` غير فارغ.

### 2.4 المواد والطلبات
- `material_requests`: `seq_code`, `project_id`, `requested_by`, `status`, `needed_date`, `supplier_id?`, `approval_status`, `approval_at`, `approval_by`.
- `material_request_items`: `request_id`, `catalog_item_id`, `description`, `quantity`, `unit`, `unit_price_estimate`.
- `material_returns`: بنية مشابهة مع `return_reason`.
- `material_return_items`: مشابه للطلبات مع كمية مرتجعة.

### 2.5 المشتريات والمدفوعات
- `purchase_orders`: `seq_code`, `project_id`, `supplier_id`, `status`, `total_amount`, `currency`, `approval_status`, `delivery_date`.
- `purchase_order_items`: ترتبط بالطلبات أو بالـ BOQ.
- `payment_orders`: `seq_code`, `project_id`, `supplier_id`, `amount`, `currency`, `payment_date`, `status`, `related_po_id`.
- `payment_ledger_entries`: تسجّل المدفوعات التفصيلية، طريقة الدفع، المستندات المرفقة.

### 2.6 الكيانات الداعمة
- `suppliers`, `contractors`, `catalog_items`: معلومات الاتصال، التصنيفات، ملاحظات، حالة التفعيل.
- `attachments`: تعريف داخلي قبل الربط بـ Drive.
- `attachment_links`: `attachment_id`, `drive_file_id`, `version`, `uploaded_by`, `tags` (array), `is_latest`.

### 2.7 الإشعارات والإعدادات
- `notifications`: `user_id`, `channel`, `type`, `payload_json`, `read_at`, `sent_at`.
- `notification_preferences`: قنوات مفعلة، فترات الهدوء، أنواع الأحداث.
- `saved_views`: الاستعلام، اسم العرض، `shared_with`.
- `system_settings`: تكوين عالمي (Drive، النسخ، المساعد، القوالب).

### 2.8 التسلسل والترقيم
- `sequence_counters`: `type`, `year`, `current_value`، وظيفة لضمان الذرية عبر Postgres function.

### 2.9 المساعد الذكي
- `ai_sessions`: `id`, `user_id`, `context`, `created_at`.
- `ai_messages`: `session_id`, `role`, `content`, `metadata` (يخزن الصفحة/الكيان، مع إخفاء القيم المالية للـ Trial).
- `ai_settings`: مفاتيح API، السماح لكل دور.

## 3. القيود والتحقق
- **الكميات والأسعار**: CHECK (`quantity > 0`, `unit_price >= 0`).
- **التواريخ**: CHECK (`end_date >= start_date`)، `delivery_date >= current_date` (مرن).
- **التفرّد**: `UNIQUE (project_id, code)` للأكواد، `UNIQUE(seq_code)` عالمي.
- **سياسات التجربة**: View يحل محل القيم المالية بالأصفار أو نصوص مشفرة عند الدور `trial` باستخدام Views أو Functions خاصة.

## 4. التدقيق والأرشفة
- `audit_logs`: `id`, `user_id`, `action`, `entity`, `entity_id`, `before`, `after`, `request_ip`, `user_agent`, `created_at`.
- وظائف Trigger على INSERT/UPDATE/DELETE لتعبئة السجل، مع استثناء admin عند الحذف النهائي.
- واجهة تعرض السجل لكل سجل، وبحث عالمي للمسؤول.

## 5. الاستيراد/التصدير
- جداول إضافية:
  - `import_jobs`: الحالة، نوع الكيان، المستخدم، النتائج، أخطاء، خريطة الأعمدة.
  - `import_job_rows`: سطر لكل صف مع حالة (OK/Warning/Error) ورسائل باللغة العربية.
  - `export_jobs`: نوع الكيان، المعلمات، حالة التوليد، رابط الملف.
- تخزين القوالب في جدول `import_templates` مع إعدادات الأعمدة والرموز البديلة.

## 6. النسخ الاحتياطي
- `backup_jobs`: نوع النسخة (يومي/يدوي)، نطاق البيانات، الموقع (Drive/Local)، `status`, `size`, `checksum`, `encrypted_key_ref`.
- `backup_settings`: وقت التنفيذ، الاحتفاظ، مجلد Drive.

