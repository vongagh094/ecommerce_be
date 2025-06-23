"use client"

import { useState } from "react"
import { useToast } from "@/hooks/use-toast"
import { AddCatalogModal } from "@/components/modals/add-catalog-modal"
import { EditCatalogModal } from "@/components/modals/edit-catalog-modal"
import { DeleteCatalogModal } from "@/components/modals/delete-catalog-modal"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Plus, Search, Eye, Edit, Trash2, FolderOpen, Filter, ChevronRight, ChevronDown, Folder } from "lucide-react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface Catalog {
  id: string
  name: string
  description: string
  type: string
  itemCount: number
  level: number
  status: string
  parentId?: string
  children?: Catalog[]
  expanded?: boolean
}

export default function Catalog() {
  const [addModal, setAddModal] = useState({ open: false, parentId: "" })
  const [editModal, setEditModal] = useState({ open: false, catalog: { id: "", name: "", description: "", type: "" } })
  const [deleteModal, setDeleteModal] = useState({ open: false, catalog: { id: "", name: "", itemCount: 0 } })
  const [viewMode, setViewMode] = useState<"grid" | "tree">("grid")
  const { toast } = useToast()

  const [catalogs, setCatalogs] = useState<Catalog[]>([
    {
      id: "1",
      name: "Residential Properties",
      description: "All types of residential accommodations",
      type: "residential",
      itemCount: 45,
      level: 0,
      status: "active",
      expanded: true,
      children: [
        {
          id: "1-1",
          name: "Apartments",
          description: "Modern apartment units",
          type: "residential",
          itemCount: 25,
          level: 1,
          status: "active",
          parentId: "1",
        },
        {
          id: "1-2",
          name: "Houses",
          description: "Single family houses",
          type: "residential",
          itemCount: 20,
          level: 1,
          status: "active",
          parentId: "1",
        },
      ],
    },
    {
      id: "2",
      name: "Commercial Properties",
      description: "Business and commercial spaces",
      type: "commercial",
      itemCount: 18,
      level: 0,
      status: "active",
      expanded: false,
      children: [
        {
          id: "2-1",
          name: "Office Spaces",
          description: "Professional office buildings",
          type: "commercial",
          itemCount: 12,
          level: 1,
          status: "active",
          parentId: "2",
        },
        {
          id: "2-2",
          name: "Retail Spaces",
          description: "Shopping and retail locations",
          type: "commercial",
          itemCount: 6,
          level: 1,
          status: "active",
          parentId: "2",
        },
      ],
    },
    {
      id: "3",
      name: "Vacation Rentals",
      description: "Short-term vacation accommodations",
      type: "vacation",
      itemCount: 32,
      level: 0,
      status: "active",
      expanded: false,
      children: [
        {
          id: "3-1",
          name: "Beach Properties",
          description: "Beachfront vacation rentals",
          type: "vacation",
          itemCount: 15,
          level: 1,
          status: "active",
          parentId: "3",
        },
        {
          id: "3-2",
          name: "Mountain Cabins",
          description: "Mountain and forest cabins",
          type: "vacation",
          itemCount: 10,
          level: 1,
          status: "active",
          parentId: "3",
        },
        {
          id: "3-3",
          name: "City Apartments",
          description: "Urban vacation apartments",
          type: "vacation",
          itemCount: 7,
          level: 1,
          status: "active",
          parentId: "3",
        },
      ],
    },
  ])

  const handleAddCatalog = (parentId = "") => {
    setAddModal({ open: true, parentId })
  }

  const handleEditCatalog = (catalog: any) => {
    setEditModal({ open: true, catalog })
  }

  const handleDeleteCatalog = (catalog: any) => {
    setDeleteModal({ open: true, catalog: { id: catalog.id, name: catalog.name, itemCount: catalog.itemCount } })
  }

  const handleViewCatalog = (catalogId: string) => {
    toast({
      title: "View Catalog",
      description: `Viewing catalog ${catalogId}...`,
    })
  }

  const toggleExpanded = (catalogId: string) => {
    setCatalogs((prev) => prev.map((cat) => (cat.id === catalogId ? { ...cat, expanded: !cat.expanded } : cat)))
  }

  const onAddConfirm = (name: string, description: string, type: string) => {
    const newCatalog: Catalog = {
      id: Date.now().toString(),
      name,
      description,
      type,
      itemCount: 0,
      level: addModal.parentId ? 1 : 0,
      status: "active",
      parentId: addModal.parentId || undefined,
    }

    if (addModal.parentId) {
      // Add as child
      setCatalogs((prev) =>
        prev.map((cat) =>
          cat.id === addModal.parentId ? { ...cat, children: [...(cat.children || []), newCatalog] } : cat,
        ),
      )
    } else {
      // Add as root catalog
      setCatalogs((prev) => [...prev, newCatalog])
    }

    toast({
      title: "Catalog Created",
      description: `${name} has been created successfully.`,
    })
  }

  const onEditConfirm = (id: string, name: string, description: string, type: string) => {
    const updateCatalog = (catalogs: Catalog[]): Catalog[] => {
      return catalogs.map((cat) => {
        if (cat.id === id) {
          return { ...cat, name, description, type }
        }
        if (cat.children) {
          return { ...cat, children: updateCatalog(cat.children) }
        }
        return cat
      })
    }

    setCatalogs((prev) => updateCatalog(prev))
    toast({
      title: "Catalog Updated",
      description: `${name} has been updated successfully.`,
    })
  }

  const onDeleteConfirm = (id: string) => {
    const deleteCatalog = (catalogs: Catalog[]): Catalog[] => {
      return catalogs
        .filter((cat) => cat.id !== id)
        .map((cat) => ({
          ...cat,
          children: cat.children ? deleteCatalog(cat.children) : undefined,
        }))
    }

    setCatalogs((prev) => deleteCatalog(prev))
    toast({
      title: "Catalog Deleted",
      description: "Catalog has been deleted successfully.",
      variant: "destructive",
    })
  }

  const renderTreeView = () => {
    const renderCatalogTree = (catalog: Catalog, depth = 0) => (
      <div key={catalog.id} className="space-y-2">
        <div
          className={`flex items-center gap-2 p-3 rounded-lg border hover:bg-gray-50 ${
            depth > 0 ? "ml-6 border-l-2 border-blue-200" : ""
          }`}
        >
          <div className="flex items-center gap-2 flex-1">
            {catalog.children && catalog.children.length > 0 ? (
              <Button variant="ghost" size="sm" onClick={() => toggleExpanded(catalog.id)} className="p-1 h-6 w-6">
                {catalog.expanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
              </Button>
            ) : (
              <div className="w-6" />
            )}

            <div className="w-8 h-8 bg-blue-100 rounded flex items-center justify-center">
              {catalog.children && catalog.children.length > 0 ? (
                <FolderOpen className="w-4 h-4 text-blue-500" />
              ) : (
                <Folder className="w-4 h-4 text-blue-500" />
              )}
            </div>

            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span className="font-medium">{catalog.name}</span>
                <Badge className="bg-green-100 text-green-800 text-xs">{catalog.status}</Badge>
              </div>
              <div className="text-sm text-gray-500">{catalog.itemCount} items</div>
            </div>
          </div>

          <div className="flex items-center gap-1">
            <Button size="sm" variant="ghost" onClick={() => handleAddCatalog(catalog.id)}>
              <Plus className="w-4 h-4" />
            </Button>
            <Button size="sm" variant="ghost" onClick={() => handleViewCatalog(catalog.id)}>
              <Eye className="w-4 h-4" />
            </Button>
            <Button size="sm" variant="ghost" onClick={() => handleEditCatalog(catalog)}>
              <Edit className="w-4 h-4" />
            </Button>
            <Button size="sm" variant="ghost" className="text-red-500" onClick={() => handleDeleteCatalog(catalog)}>
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {catalog.expanded && catalog.children && (
          <div className="space-y-2">{catalog.children.map((child) => renderCatalogTree(child, depth + 1))}</div>
        )}
      </div>
    )

    return <div className="space-y-4">{catalogs.map((catalog) => renderCatalogTree(catalog))}</div>
  }

  const renderGridView = () => {
    const getAllCatalogs = (catalogs: Catalog[]): Catalog[] => {
      const result: Catalog[] = []
      catalogs.forEach((catalog) => {
        result.push(catalog)
        if (catalog.children) {
          result.push(...getAllCatalogs(catalog.children))
        }
      })
      return result
    }

    const allCatalogs = getAllCatalogs(catalogs)

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {allCatalogs.map((catalog) => (
          <Card key={catalog.id} className="relative">
            <div className="absolute top-4 left-4 flex gap-2">
              <Badge className="bg-green-100 text-green-800">{catalog.status}</Badge>
              {catalog.level > 0 && <Badge variant="outline">Level {catalog.level}</Badge>}
            </div>
            <div className="absolute top-4 right-4 flex gap-2">
              <Button size="sm" variant="ghost" onClick={() => handleAddCatalog(catalog.id)}>
                <Plus className="w-4 h-4" />
              </Button>
              <Button size="sm" variant="ghost" onClick={() => handleViewCatalog(catalog.id)}>
                <Eye className="w-4 h-4" />
              </Button>
              <Button size="sm" variant="ghost" onClick={() => handleEditCatalog(catalog)}>
                <Edit className="w-4 h-4" />
              </Button>
              <Button size="sm" variant="ghost" className="text-red-500" onClick={() => handleDeleteCatalog(catalog)}>
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
            <CardContent className="pt-16 pb-6">
              <div className="text-center mb-4">
                <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  {catalog.children && catalog.children.length > 0 ? (
                    <FolderOpen className="w-8 h-8 text-blue-500" />
                  ) : (
                    <Folder className="w-8 h-8 text-blue-500" />
                  )}
                </div>
                <h3 className="font-semibold text-lg">{catalog.name}</h3>
                <p className="text-sm text-gray-500 mt-1">{catalog.description}</p>
                <div className="flex items-center justify-between mt-4 text-sm text-gray-500">
                  <span>{catalog.itemCount} items</span>
                  <span>Level {catalog.level}</span>
                </div>
                {catalog.parentId && (
                  <div className="text-xs text-blue-600 mt-1">
                    Subcategory of {catalogs.find((c) => c.id === catalog.parentId)?.name}
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Catalog Management</h1>
          <div className="text-sm text-gray-500">Home &gt; Catalog</div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant={viewMode === "tree" ? "default" : "outline"} onClick={() => setViewMode("tree")}>
            Tree View
          </Button>
          <Button variant={viewMode === "grid" ? "default" : "outline"} onClick={() => setViewMode("grid")}>
            Grid View
          </Button>
          <Button className="bg-blue-500 hover:bg-blue-600" onClick={() => handleAddCatalog()}>
            <Plus className="w-4 h-4 mr-2" />
            Add Catalog
          </Button>
        </div>
      </div>

      <div className="flex items-center gap-2 text-sm text-gray-600">
        <FolderOpen className="w-4 h-4" />
        All Categories
      </div>

      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input placeholder="Search catalogs..." className="pl-10" />
        </div>
        <Select defaultValue="all">
          <SelectTrigger className="w-40">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="inactive">Inactive</SelectItem>
          </SelectContent>
        </Select>
        <Button variant="outline">
          <Filter className="w-4 h-4 mr-2" />
          More Filters
        </Button>
      </div>

      {viewMode === "tree" ? renderTreeView() : renderGridView()}

      <AddCatalogModal
        open={addModal.open}
        onOpenChange={(open) => setAddModal((prev) => ({ ...prev, open }))}
        onConfirm={onAddConfirm}
        parentId={addModal.parentId}
      />

      <EditCatalogModal
        open={editModal.open}
        onOpenChange={(open) => setEditModal((prev) => ({ ...prev, open }))}
        catalog={editModal.catalog}
        onConfirm={onEditConfirm}
      />

      <DeleteCatalogModal
        open={deleteModal.open}
        onOpenChange={(open) => setDeleteModal((prev) => ({ ...prev, open }))}
        catalog={deleteModal.catalog}
        onConfirm={onDeleteConfirm}
      />
    </div>
  )
}
