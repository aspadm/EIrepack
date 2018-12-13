import collada as dae

def merge_dae_files(list_fpath_inputs, fpath_output, scene_name="myscene"):
    list_dae_objects = []
    
    for fpath_input in list_fpath_inputs:
        list_dae_objects.append(dae.Collada(fpath_input))
        
    merged_dae_object = merge_dae_objects(list_dae_objects, scene_name="myscene")
    merged_dae_object.write(fpath_output)

def merge_dae_objects(list_dae_objects, scene_name):
    merged_dae_object = dae.Collada()  
    
    if len(list_dae_objects) == 0:
        return merged_dae_object
   
    merged_dae_object.assetInfo = list_dae_objects[-1].assetInfo
    merged_dae_object.lights.extend(list_dae_objects[-1].lights)
    
    list_nodes_of_scene = []
    for mesh in list_dae_objects:
        merged_dae_object.effects.extend(mesh.effects)
        merged_dae_object.materials.extend(mesh.materials)
        merged_dae_object.images.extend(mesh.images)
        merged_dae_object.geometries.extend(mesh.geometries)
       
        for scene in mesh.scenes:
            list_nodes_of_scene.extend(scene.nodes)         
       
    myscene = dae.scene.Scene(scene_name, list_nodes_of_scene)
    merged_dae_object.scenes.append(myscene)
    merged_dae_object.scene = myscene       
           
    return merged_dae_object
