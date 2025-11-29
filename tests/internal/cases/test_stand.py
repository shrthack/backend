import uuid
import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from src.internal.cases.stand import create_stand, get_stand, get_all_stands, update_stand, delete_stand
from src.internal.entities.stand import CreateStand, UpdateStand
from src.db import models as m


@pytest.fixture
def mock_session():
    """Mock AsyncSession for testing."""
    session = AsyncMock(spec=AsyncSession)
    session.begin.return_value.__aenter__ = AsyncMock()
    session.begin.return_value.__aexit__ = AsyncMock(return_value=None)
    return session


@pytest.fixture
def sample_stand():
    """Sample stand data for testing."""
    return m.Stand(
        id=uuid.uuid4(),
        name="Sample Stand",
        info="This is a sample stand",
        location="Main Hall",
        image_url="http://example.com/stand.jpg"
    )


@pytest.fixture
def create_stand_data():
    """Sample CreateStand data."""
    return CreateStand(
        name="Sample Stand",
        info="This is a sample stand",
        location="Main Hall",
        image_url="http://example.com/stand.jpg"
    )


@pytest.fixture
def update_stand_data():
    """Sample UpdateStand data."""
    return UpdateStand(
        name="Updated Stand",
        info=None,
        location="Updated Location",
        image_url="http://example.com/updated_stand.jpg"
    )


class TestCreateStand:
    @pytest.mark.asyncio
    async def test_create_stand_success(self, mock_session, sample_stand, create_stand_data):
        # Arrange
        with patch('internal.cases.stand.s.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.create_stand.return_value = sample_stand
            mock_querier_class.return_value = mock_querier

            # Act
            result = await create_stand(mock_session, create_stand_data)

            # Assert
            assert result == sample_stand
            mock_querier.create_stand.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_stand_failure(self, mock_session, create_stand_data):
        # Arrange
        with patch('internal.cases.stand.s.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.create_stand.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await create_stand(mock_session, create_stand_data)

            # Assert
            assert result is None
            mock_querier.create_stand.assert_called_once()


class TestGetStand:
    @pytest.mark.asyncio
    async def test_get_stand_success(self, mock_session, sample_stand):
        # Arrange
        stand_id = sample_stand.id
        with patch('internal.cases.stand.s.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_stand_by_id.return_value = sample_stand
            mock_querier_class.return_value = mock_querier

            # Act
            result = await get_stand(mock_session, stand_id)

            # Assert
            assert result == sample_stand
            mock_querier.get_stand_by_id.assert_called_once_with(id=stand_id)

    @pytest.mark.asyncio
    async def test_get_stand_not_found(self, mock_session):
        # Arrange
        stand_id = uuid.uuid4()
        with patch('internal.cases.stand.s.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_stand_by_id.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await get_stand(mock_session, stand_id)

            # Assert
            assert result is None
            mock_querier.get_stand_by_id.assert_called_once_with(id=stand_id)


class TestGetAllStands:
    @pytest.mark.asyncio
    async def test_get_all_stands(self, mock_session, sample_stand):
        # Arrange
        stands = [sample_stand]

        async def mock_async_iter():
            for stand in stands:
                yield stand

        with patch('internal.cases.stand.s.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_all_stands = mock_async_iter
            mock_querier_class.return_value = mock_querier

            # Act
            result = []
            async for stand in get_all_stands(mock_session):
                result.append(stand)

            # Assert
            assert result == stands

    @pytest.mark.asyncio
    async def test_get_all_stands_empty(self, mock_session):
        # Arrange
        async def mock_async_iter():
            return
            yield  # pragma: no cover

        with patch('internal.cases.stand.s.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_all_stands = mock_async_iter
            mock_querier_class.return_value = mock_querier

            # Act
            result = []
            async for stand in get_all_stands(mock_session):
                result.append(stand)

            # Assert
            assert result == []


class TestUpdateStand:
    @pytest.mark.asyncio
    async def test_update_stand_success(self, mock_session, sample_stand, update_stand_data):
        # Arrange
        stand_id = sample_stand.id
        updated_stand = m.Stand(
            id=stand_id,
            name="Updated Stand",
            info=sample_stand.info,
            location="Updated Location",
            image_url="http://example.com/updated_stand.jpg"
        )
        with patch('internal.cases.stand.s.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.update_stand.return_value = updated_stand
            mock_querier_class.return_value = mock_querier

            # Act
            result = await update_stand(mock_session, stand_id, update_stand_data)

            # Assert
            assert result == updated_stand
            mock_querier.update_stand.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_stand_not_found(self, mock_session, update_stand_data):
        # Arrange
        stand_id = uuid.uuid4()
        with patch('internal.cases.stand.s.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.update_stand.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await update_stand(mock_session, stand_id, update_stand_data)

            # Assert
            assert result is None
            mock_querier.update_stand.assert_called_once()


class TestDeleteStand:
    @pytest.mark.asyncio
    async def test_delete_stand_success(self, mock_session):
        # Arrange
        stand_id = uuid.uuid4()
        with patch('internal.cases.stand.s.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.delete_stand.return_value = None  # delete_stand doesn't return anything in the code
            mock_querier_class.return_value = mock_querier

            # Act
            result = await delete_stand(mock_session, stand_id)

            # Assert
            assert result is True
            mock_querier.delete_stand.assert_called_once_with(id=stand_id)