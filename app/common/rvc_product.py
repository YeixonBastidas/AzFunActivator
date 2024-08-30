def products_colabora_vtex(id_product: int): 
        switcher = {
            55600: 1, # bar codes for products
            55603: 1, # bar codes GLN
            55602: 1, # bar codes variable weight
            55800: 1  # Bar codes documents
        }
        id_product_final = switcher.get(id_product, id_product)
        return id_product_final