from product.models import ProductClass, ProductCategory


def getMenu():
# It will only fetch the details of one product
    productClasses = ProductClass.objects.all().filter(isActive=True)
    productCategories = ProductCategory.objects.all()
    classMenuDict = {

    }
    for productClass in productClasses:
        className = productClass.name
        classId = productClass.id
        classMenuDict.update({classId: className})

    context = {
        'classMenuDict': classMenuDict,
        'productCategories': productCategories,
        # 'product': product
    }
    return context


