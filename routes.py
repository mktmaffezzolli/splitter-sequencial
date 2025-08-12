from flask import Blueprint, request, jsonify, redirect
from models import URLSplit, db
import json

url_split_bp = Blueprint('url_split', __name__)

# Contador global para distribuição sequencial
split_counters = {}

def safe_json_parse(data):
    """Parse seguro de JSON"""
    try:
        if isinstance(data, list):
            return data
        if isinstance(data, str):
            parsed = json.loads(data)
            if isinstance(parsed, str):
                parsed = json.loads(parsed)
            return parsed if isinstance(parsed, list) else []
        return []
    except:
        return []

def get_next_destination(split_id, destinations):
    """Obtém próximo destino na sequência"""
    global split_counters
    
    if split_id not in split_counters:
        split_counters[split_id] = 0
    
    # Índice atual
    index = split_counters[split_id] % len(destinations)
    
    # Incrementar para próximo
    split_counters[split_id] += 1
    
    return index, destinations[index]

@url_split_bp.route('/splits', methods=['GET'])
def get_splits():
    """Listar todos os splits"""
    try:
        splits = URLSplit.query.all()
        result = []
        
        for split in splits:
            destinations = safe_json_parse(split.destinations)
            result.append({
                'id': split.id,
                'slug': split.slug,
                'name': split.name,
                'destinations': destinations,
                'created_at': split.created_at.isoformat(),
                'total_destinations': len(destinations)
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@url_split_bp.route('/splits', methods=['POST'])
def create_split():
    """Criar novo split"""
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('slug'):
            return jsonify({'error': 'Slug é obrigatório'}), 400
        
        if not data.get('name'):
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        if not data.get('destinations') or len(data['destinations']) == 0:
            return jsonify({'error': 'Pelo menos um destino é obrigatório'}), 400
        
        # Verificar se slug já existe
        if URLSplit.query.filter_by(slug=data['slug']).first():
            return jsonify({'error': 'Slug já existe'}), 400
        
        # Criar split
        new_split = URLSplit(
            slug=data['slug'],
            name=data['name'],
            destinations=json.dumps(data['destinations'])
        )
        
        db.session.add(new_split)
        db.session.commit()
        
        return jsonify({
            'id': new_split.id,
            'slug': new_split.slug,
            'name': new_split.name,
            'message': 'Split criado com sucesso'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@url_split_bp.route('/splits/<int:split_id>', methods=['DELETE'])
def delete_split(split_id):
    """Deletar split"""
    try:
        split = URLSplit.query.get(split_id)
        if not split:
            return jsonify({'error': 'Split não encontrado'}), 404
        
        # Remover do contador também
        global split_counters
        if split.id in split_counters:
            del split_counters[split.id]
        
        db.session.delete(split)
        db.session.commit()
        
        return jsonify({'message': 'Split deletado com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@url_split_bp.route('/r/<slug>')
def redirect_split(slug):
    """🔄 REDIRECIONAMENTO SEQUENCIAL"""
    try:
        print(f"🔍 REDIRECIONAMENTO SEQUENCIAL: {slug}")
        
        # Buscar split
        split = URLSplit.query.filter_by(slug=slug).first()
        if not split:
            return jsonify({'error': 'Split não encontrado'}), 404
        
        # Parse destinos
        destinations = safe_json_parse(split.destinations)
        if not destinations:
            return jsonify({'error': 'Nenhum destino configurado'}), 404
        
        # Obter próximo destino sequencial
        index, chosen_url = get_next_destination(split.id, destinations)
        
        print(f"🎯 Split: {slug} | Destino {index + 1}/{len(destinations)}: {chosen_url}")
        
        return redirect(chosen_url, code=302)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return jsonify({'error': 'Erro interno'}), 500

@url_split_bp.route('/debug/counters')
def debug_counters():
    """Debug dos contadores sequenciais"""
    global split_counters
    
    splits = URLSplit.query.all()
    debug_data = []
    
    for split in splits:
        destinations = safe_json_parse(split.destinations)
        counter = split_counters.get(split.id, 0)
        next_index = counter % len(destinations) if destinations else 0
        
        debug_data.append({
            'split_id': split.id,
            'slug': split.slug,
            'total_destinations': len(destinations),
            'current_counter': counter,
            'next_destination_index': next_index + 1,
            'destinations': destinations
        })
    
    return jsonify({
        'counters': split_counters,
        'splits': debug_data
    })
    
@url_split_bp.route('/splits/<int:split_id>', methods=['PUT'])
def update_split(split_id):
    """Atualizar split existente"""
    try:
        data = request.get_json()
        
        # Validações
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        name = data.get('name', '').strip()
        destinations = data.get('destinations', [])
        
        if not name:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        if not destinations or len(destinations) < 1:
            return jsonify({'error': 'Pelo menos um destino é obrigatório'}), 400
        
        # Buscar split existente
        split = URLSplit.query.get(split_id)
        if not split:
            return jsonify({'error': 'Split não encontrado'}), 404
        
        # Atualizar dados
        split.name = name
        split.destinations = json.dumps(destinations)
        split.updated_at = datetime.utcnow()
        
        # Salvar no banco
        db.session.commit()
        
        print(f"✅ Split {split.slug} atualizado com sucesso")
        
        return jsonify({
            'message': 'Split atualizado com sucesso',
            'split': {
                'id': split.id,
                'slug': split.slug,
                'name': split.name,
                'destinations': destinations,
                'url': f'/api/r/{split.slug}'
            }
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao atualizar split: {e}")
        return jsonify({'error': str(e)}), 500
