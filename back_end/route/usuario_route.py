from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from back_end.models.usuario_models import Usuario
from back_end.dtos.usuario_dtos import UsuarioCriar, UsuarioResposta
from back_end.create_db import get_db


router = APIRouter()

# Função para retornar todos os usuários
@router.get("/usuarios/", response_model=list[UsuarioResposta])
async def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    if not usuarios:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado.")
    return usuarios


# Função para retornar um usuário específico por ID
@router.get("/usuarios/{usuario_id}", response_model=UsuarioResposta)
async def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    # Busca o usuário no banco de dados
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuário Id {usuario_id}")
    return usuario

# Função para criar um usuário
@router.post("/usuarios/", response_model=UsuarioResposta)
async def criar_usuario(usuario: UsuarioCriar, db: Session = Depends(get_db)):
    try:
        # Verifica se o CPF já está cadastrado
        cpf_existente = db.query(Usuario).filter(Usuario.cpf == usuario.cpf).first()
        if cpf_existente:
            raise HTTPException(status_code=400, detail="CPF já cadastrado em outro usuario")
                
        # Cria o novo usuário usando o DTO de entrada
        novo_usuario = Usuario(
            nome=usuario.nome,
            perfil=usuario.perfil,
            email=usuario.email, 
            cpf=usuario.cpf,
            telefone=usuario.telefone,
            senha=usuario.senha,
            cep=usuario.cep,
            rua=usuario.rua,
            numero=usuario.numero,
            bairro=usuario.bairro,
            complemento=usuario.complemento,
            cidade=usuario.cidade,
            estado=usuario.estado,
        )
        
        # Adiciona o usuário ao banco de dados
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        # Retorna a resposta com o DTO de saída (UsuarioResposta)
        return novo_usuario  
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)} ao criar usuário!")


# Função para atualizar um usuário por id  
@router.put("/usuarios/{usuario_id}", response_model=UsuarioResposta)
def atualizar_usuario(usuario_id: int, usuario: UsuarioCriar, db: Session = Depends(get_db)):
    # Busca o usuário pelo ID no banco de dados
    usuario_existente = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario_existente:
       raise HTTPException(status_code=404, detail="Usuário não encontrado")
    for field, value in usuario.dict(exclude_unset=True).items():
        setattr(usuario_existente, field, value)

    db.add(usuario_existente)  
    db.commit()                
    db.refresh(usuario_existente) 
 
    return usuario_existente  

# Função para atualizar um usuário por id com incremento do handler falta testar
# @router.put("/usuarios/{usuario_id}", response_model=UsuarioResposta)
# def atualizar_usuario(usuario_id: int, usuario: UsuarioCriar, db: Session = Depends(get_db)):
#     try:
#         # Busca o usuário pelo ID no banco de dados
#         usuario_existente = db.query(Usuario).filter(Usuario.id == usuario_id).first()

#         if not usuario_existente:
#             raise HTTPException(status_code=404, detail="Usuário não encontrado")

#         for field, value in usuario.dict(exclude_unset=True).items():
#             setattr(usuario_existente, field, value)

#         db.add(usuario_existente)  
#         db.commit()                
#         db.refresh(usuario_existente) 

#         return usuario_existente

#     except HTTPException as e:
#         raise e  # O handler genérico irá tratar isso

#     except Exception as e:
#         db.rollback()
#         logger.error(f"Erro inesperado ao atualizar usuário: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Erro {str(e)} ao atualizar usuário!")

# Função para deletar um usuário por id 
@router.delete("/usuarios/{usuario_id}", status_code=200)
async def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        # Lançando a exceção que será tratada no error_handlers.py
        raise HTTPException(status_code=404, detail=f"Usuário com ID {usuario_id} não encontrado")

    # Remove o usuário
    db.delete(usuario)
    db.commit()
    
    # Retorna apenas uma mensagem de sucesso
    return {"message": f"Usuário com ID {usuario_id} deletado com sucesso!"}