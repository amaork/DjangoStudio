# DjangoStudio

使用 Django 作为后台框架，前端使用 Bootstrap，为个人工作室提供信息展示服务，工程下包含两个 App: core、homepage。

## core

提供一些基础的 Model 和 Admin 基类

#### Model

**`Document`**: FileField Model 的封装，提供文件上传功能

**`Message`**：保存用户从网页上提交的留言信息，有对应的`UserMessageForm`

**`Gallery`**：相册，可以为每张图片设置描述信息，可以控制选择是否在导航栏显示

**`Picture`**：相册照片，每个照片都要指定属于哪个相册，可以为照片设置描述信息

**`Navigation`** ：导航栏与 `NavigationModel`配合使用，可以调整显示的位置
 
**`NavigationModel`**：继承 `NavigationModel` 后，重载 `url`, `text` 在保存模块的时候将会自动创建 `Navigation` Instance。`url`是导航链接或锚的地址，`text` 是链接或锚显示的文字信息，`is_anchor`用来确定该导航信息是锚还是超链接， `parent`是用来指定锚的父页面的链接地址。

例如:
	
	homepage/#about 是 homepage 下一个锚的地址
	
	那么在 url="about", parent="homepage", is_anchor=True 
	
	在 homepage 页面下，这个导航链接表现为 /homepage/#about
	
	在 homepage 之外，这个导航链接表现为 /homepage/anchor/about
	
	在 homepage 之外，core.urls 会自动处理这种情况将其重定位到 /homepage/#about 地址
	
#### Admin

**`LimitInstanceAdmin`**: 继承该类可以限制 Model 创建 Instance 的数量

**`OrderedModelAdmin`**: 继承该类为 Model Instance 添加排序管理的 Actions

**`LimitInlineInstanceAdmin`**: 继承该类可以限制 Model 创建 StackedInline Instance 的数量


## homepage

工作室信息展示，默认包含一下几个版块：关于我们、服务项目、客户评价、付费计划、联系我们。每个版块都有对应的数据 Model。

**`Service`**：可以创建多个实例，对应 homepage 的服务项目。

**`StudioInfo`**： 只能创建一个实例对应 homepage 的关于我们。

**`ContactInfo`**：只能创建一个实例对应 homepage 的联系我们。

**`CustomComment`**：可以创建多个实例，定义 homepage 的客户评价滚动信息。

**`PaymentPlan`**：可以创建多个实例，每个实例下可以创建多个 `PaymentItem`，指定为`StudioInfo`下的`primary_payment_plan`后可以在首页展示，对应 homepage 的付费计划。

**`PaymentItem`**：可以创建多个实例，对应付费计划下的不同子项目，每个 `PaymentItem` 必须隶属于某个`PaymentPlan`。
